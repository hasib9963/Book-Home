from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from . import views
from core import views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('readers/', include('readers.urls')),
    path('transactions/', include('transactions.urls')),

    path('category/<slug:category_slug>/', views.home, name='category_wise_book'),
    path('book/', include('books.urls')),
    path('category/', include('categories.urls')),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
