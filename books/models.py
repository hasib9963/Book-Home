from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from readers.models import UserLibraryAccount

class Book(models.Model):
    book_title = models.CharField(max_length=50)
    description = models.TextField()
    price =models.DecimalField(decimal_places=2, max_digits = 12)
    category = models.ManyToManyField(Category)
    reader = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    borrowed_by = models.ManyToManyField(User, related_name='borrowed_book', blank=True)
    images = models.ImageField(upload_to='books/media/uploads/')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.book_title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    Reviews = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Reviews by {self.name}"
