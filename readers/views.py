from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string

from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import redirect
from transactions.models import Borrow
from django.contrib.auth import logout

class UserRegistrationView(FormView):
    template_name = 'readers/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake
    

class UserLoginView(LoginView):
    template_name = 'readers/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')




def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse_lazy('home'))

    
class UserProfileView(View):
    # template_name = 'readers/profile.html'

    # def get(self, request):
    #     form = UserUpdateForm(instance=request.user)
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request):
    #     form = UserUpdateForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile')  # Redirect to the user's profile page
    #     return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        user_account = request.user.account
        borrowed_books = Borrow.objects.filter(user_account=user_account)

        return render(request, 'readers/profile.html', {'borrowed_books': borrowed_books})

class UserLibraryAccountUpdateView(View):
    template_name = 'readers/update.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    


class PassChangeView(View):
    template_name = 'readers/password_change.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')

            # Send email to the user
            mail_subject = 'Password Change Notification'
            message = render_to_string('readers/password_change_message.html', {'user': request.user})
            to_email = request.user.email
            send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()

            update_session_auth_hash(request, form.user)
            return redirect('profile')

        return render(request, self.template_name, {'form': form})