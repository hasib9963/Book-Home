from django.urls import path
from . import views
urlpatterns = [

    path('add/', views.AddbookCreateView.as_view(), name='add_book'),
    path('details/<int:id>/', views.DetailBookView.as_view(), name='detail_book'),
    path('details/<int:id>/post-review/', views.DetailBookView.as_view(), name='post_review'),
]
