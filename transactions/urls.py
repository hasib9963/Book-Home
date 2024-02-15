from django.urls import path
from .views import DepositMoneyView, BorrowBookView, ReturnBookView


# app_name = 'transactions'
urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("borrow/<int:book_id>/", BorrowBookView.as_view(), name="borrow_book"),
    path('return_book/<int:borrow_id>/', ReturnBookView.as_view(), name='return_book'),
]