from django.shortcuts import redirect, get_object_or_404
from . import forms
from . import models
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView
from books.models import Review
from books.forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Book

@method_decorator(login_required, name='dispatch')
class AddbookCreateView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'add_book.html'
    success_url = reverse_lazy('add_book')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    



from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import ReviewForm


class DetailBookView(View):
    template_name = 'book_details.html'

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['id'])
        reviews = book.reviews.all()
        review_form = ReviewForm()
        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['id'])

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has borrowed the book
            print(f'User ID: {request.user.id}')
            print(f'Borrowed by user IDs: {book.borrowed_by.all().values_list("id", flat=True)}')
            if book.borrowed_by.filter(id=request.user.id).exists():
                review_form = ReviewForm(request.POST)

                if review_form.is_valid():
                    new_review = review_form.save(commit=False)
                    new_review.book = book
                    new_review.save()
                    messages.success(request, 'Your review has been added.')
                    return redirect('detail_book', id=book.id)
                else:
                    # Display form errors for debugging
                    print(review_form.errors)
                    messages.error(request, 'Failed to add review. Please try again.')

                return redirect('detail_book', id=book.id)
            else:
                messages.error(request, 'You need to borrow the book first before posting a review.')
        else:
            messages.error(request, 'Please login to borrow the book and post reviews.')

        return redirect('detail_book', id=book.id)
