from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Book, BorrowTransaction
from .serializers import (
    UserSerializer,
    BookSerializer,
    BorrowTransactionSerializer,
    BorrowTransactionCreateSerializer,
    ReturnTransactionSerializer,
)


# --- Users ---
class UserListCreateAPIView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk=pk, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk=pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        return self.partial_update(request, pk=pk, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, pk=pk, *args, **kwargs)


# --- Books ---
class BookListCreateAPIView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if book.transactions.filter(status='borrowed').exists():
            return Response(
                {"message": "Cannot delete a book that is currently borrowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Borrow Transactions ---
class BorrowTransactionListAPIView(mixins.ListModelMixin,
                                   generics.GenericAPIView):
    queryset = BorrowTransaction.objects.select_related('book', 'user').all().order_by('-id')
    serializer_class = BorrowTransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BorrowAPIView(APIView):
    """
    GET  /api/borrow/   — returns 200 OK (no body)
    POST /api/borrow/   — create a borrow transaction
    """
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BorrowTransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        book = serializer.validated_data['book']
        borrow_date = serializer.validated_data['borrow_date']

        if book.copies_available < 1:
            return Response({'detail': 'No copies available.'},
                            status=status.HTTP_400_BAD_REQUEST)

        tx = BorrowTransaction.objects.create(
            user=user,
            book=book,
            borrow_date=borrow_date,
            status='borrowed'
        )
        output = BorrowTransactionSerializer(tx)
        return Response(output.data, status=status.HTTP_201_CREATED)


class ReturnAPIView(APIView):
    """
    GET  /api/return/<pk>/   — returns 200 OK (no body)
    POST /api/return/<pk>/   — mark transaction returned
    """
    def get_object(self, pk):
        return get_object_or_404(BorrowTransaction, pk=pk)

    def get(self, request, pk):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk):
        tx = self.get_object(pk)
        if tx.status == 'returned':
            return Response({'detail': 'Already returned.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ReturnTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tx.return_date = serializer.validated_data['return_date']
        tx.status = 'returned'
        tx.save()

        output = BorrowTransactionSerializer(tx)
        return Response(output.data)


