from django.urls import path
from .views import UserViewSet, BookViewSet, BorrowTransactionViewSet

user_list   = UserViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail = UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

book_list   = BookViewSet.as_view({'get': 'list', 'post': 'create'})
book_detail = BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

tx_list   = BorrowTransactionViewSet.as_view({'get': 'list'})
tx_detail = BorrowTransactionViewSet.as_view({'get': 'retrieve'})

tx_borrow = BorrowTransactionViewSet.as_view({'post': 'borrow'})
tx_return = BorrowTransactionViewSet.as_view({'post': 'return_book'})

urlpatterns = [
    path('api/users/',          user_list,    name='user-list'),
    path('api/users/<int:pk>/', user_detail,  name='user-detail'),

    path('api/books/',          book_list,    name='book-list'),
    path('api/books/<int:pk>/', book_detail,  name='book-detail'),

    path('api/transactions/',          tx_list,    name='tx-list'),
    path('api/transactions/<int:pk>/', tx_detail,  name='tx-detail'),

    path('api/borrow/',          tx_borrow, name='tx-borrow'),
    path('api/return/<int:pk>/', tx_return, name='tx-return'),
]