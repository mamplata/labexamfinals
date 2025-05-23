from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import date
from .models import Book, BorrowTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class BookSerializer(serializers.ModelSerializer):
    is_borrowed = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available', 'is_borrowed']

    def get_is_borrowed(self, obj):
        return obj.transactions.filter(status='borrowed').exists()

class BorrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = '__all__'
        read_only_fields = ['status', 'return_date']

class BorrowTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = ['user', 'book', 'borrow_date']

    def validate_borrow_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Future dates are not allowed for borrowing."
            )
        return value

class ReturnTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = ['return_date']

    def validate(self, data):
        instance = self.instance
        if instance and data['return_date'] < instance.borrow_date:
            raise serializers.ValidationError(
                "Return date cannot be earlier than borrow date."
            )
        return data