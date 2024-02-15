from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        # fields = '__all__'
        exclude = ['reader', 'borrowed_by']
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','Reviews']

