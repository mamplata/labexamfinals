from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, BorrowTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = '__all__'
        read_only_fields = ['status', 'return_date']

class BorrowTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = ['user', 'book', 'borrow_date']

class ReturnTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = ['return_date']