from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MyUserCreationForm


class MyUserCreationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')


class MyLoginView(auth_views.LoginView):
    template_name = 'users/login.html'


class MyLogoutView(auth_views.LogoutView):
    template_name = 'users/logged_out.html'


class MyPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')


class MyPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
