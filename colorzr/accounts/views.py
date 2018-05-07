from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import RegisterForm, LoginForm


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy("home")
    template_name = "accounts/login_user.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register_user.html"
