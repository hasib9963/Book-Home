from django.db import models
from .constants import TRANSACTION_TYPE

class Transaction(models.Model):
    account = models.ForeignKey('readers.UserLibraryAccount', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Borrow(models.Model):
    user_account = models.ForeignKey('readers.UserLibraryAccount', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    borrow_price = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_borrowing_book = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)

    def is_returned(self):
        return self.return_date is not None

    def __str__(self):
        return f'{self.user_account.user.username} - {self.book.book_title}'

