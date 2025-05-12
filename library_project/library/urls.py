from django.urls import path
from .views import (
    UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView,
    BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView,
    BorrowTransactionListAPIView, BorrowAPIView, ReturnAPIView,
)

urlpatterns = [
    # Users
    path('api/users/',          UserListCreateAPIView.as_view(),       name='user-list'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Books
    path('api/books/',          BookListCreateAPIView.as_view(),       name='book-list'),
    path('api/books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),

    # Borrow transactions
    path('api/transactions/',   BorrowTransactionListAPIView.as_view(), name='tx-list'),
    path('api/borrow/',         BorrowAPIView.as_view(),               name='tx-borrow'),
    path('api/return/<int:pk>/', ReturnAPIView.as_view(),              name='tx-return'),
]
