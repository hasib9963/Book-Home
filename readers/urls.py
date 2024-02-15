
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView,UserLibraryAccountUpdateView, PassChangeView,UserProfileView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/pass_change/', PassChangeView.as_view(), name='pass_change'),
    path('profile/update', UserLibraryAccountUpdateView.as_view(), name='update'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]