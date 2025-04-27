from django.contrib import messages
from django.shortcuts import  redirect, render, get_object_or_404
from django.views import View
from .models import Borrow
from django.utils import timezone
from django.contrib import messages
from .models import Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import CreateView
from transactions.constants import DEPOSIT, RETURN_BOOK

from transactions.forms import DepositForm


from books.models import Book
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('deposit_money')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    # success_url = '/transactions/deposit/'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ is deposited to your account successfully'
        )
        mail_subject = 'Deposit Message'
        message = render_to_string('transactions/deposite_email.html', {
            'user' : self.request.user,
            'amount': amount,
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        return super().form_valid(form)






from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.http import HttpResponseRedirect
from django.contrib import messages

class BorrowBookView(View):
    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        user_account = request.user.account

        # Check if the user has sufficient balance
        if user_account.balance < book.price:
            messages.error(request, 'You don\'t have sufficient balance to borrow this book')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Create a Borrow instance
        borrow_price = book.price
        Borrow.objects.create(user_account=user_account, book=book, quantity=1, borrow_price=borrow_price)

        # Deduct the book price from the user's account
        user_account.balance -= borrow_price
        user_account.save()

        # Update the book quantity
        book.quantity -= 1
        book.save()
        book.borrowed_by.add(request.user)
        # Send email to the user
        mail_subject = 'Book Borrowed'
        message = render_to_string('transactions/borrow_email.html', {
            'user': request.user,
            'book_title': book.book_title,
        })
        to_email = request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        # Add success message
        messages.success(request, f'{book.book_title} borrowed successfully')
        
        # Redirect to the same page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))









class ReturnBookView(View):
    def get(self, request, borrow_id):
        borrow = get_object_or_404(Borrow, id=borrow_id)

        # Update the return_date and balance_after_borrowing_book
        borrow.return_date = timezone.now()
        borrow.user_account.balance += borrow.borrow_price
        borrow.user_account.save()

        # Update the book quantity
        borrow.book.quantity += borrow.quantity
        borrow.book.save()

        # Create a Transaction for the return
        Transaction.objects.create(
            account=borrow.user_account,
            amount=borrow.borrow_price,
            balance_after_transaction=borrow.user_account.balance,
            transaction_type=RETURN_BOOK,
        )

        mail_subject = 'Book Returned'
        message = render_to_string('transactions/return_email.html', {
            'user': borrow.user_account.user,
            'book_title': borrow.book.book_title,
        })
        to_email = borrow.user_account.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        # Delete the Borrow record
        borrow.delete()

        # Add success message
        messages.success(request, f'{borrow.book.book_title} returned successfully')

        # Redirect to the user's profile or any other page
        return HttpResponseRedirect(reverse('profile'))
