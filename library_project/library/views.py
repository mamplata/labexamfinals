from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, BorrowTransaction
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    BookSerializer,
    BorrowTransactionSerializer,
    BorrowTransactionCreateSerializer,
    ReturnTransactionSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if book.transactions.filter(status='borrowed').exists():
            return Response({"message" : "Cannot delete a book that is currently borrowed."}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

class BorrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowTransaction.objects.select_related('book', 'user').all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'borrow':
            return BorrowTransactionCreateSerializer
        elif self.action == 'return_book':
            return ReturnTransactionSerializer
        return BorrowTransactionSerializer

    @action(detail=False, methods=['get', 'post'], url_path='borrow')
    def borrow(self, request):
        if request.method == 'GET':
            return Response(status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        book = serializer.validated_data['book']
        borrow_date = serializer.validated_data['borrow_date']
        if book.copies_available < 1:
            return Response({'detail': 'No copies available.'}, status=status.HTTP_400_BAD_REQUEST)
        tx = BorrowTransaction.objects.create(user=user, book=book, borrow_date=borrow_date, status='borrowed')
        output = BorrowTransactionSerializer(tx)
        return Response(output.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='return')
    def return_book(self, request, pk=None):
        if request.method == 'GET':
            return Response(status=status.HTTP_200_OK)
        tx = self.get_object()
        if tx.status == 'returned':
            return Response({'detail': 'Already returned.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx.return_date = serializer.validated_data['return_date']
        tx.status = 'returned'
        tx.save()
        output = BorrowTransactionSerializer(tx)
        return Response(output.data)