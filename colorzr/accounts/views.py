from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from friendship.models import Follow

from images.models import ImageConversion
from . import forms


class LoginView(generic.FormView):
    form_class = AuthenticationForm
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
    form_class = forms.RegisterForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register_user.html"


class ChangeProfileView(LoginRequiredMixin, View):
    # profile_form = forms.ProfileChangeForm
    template_name = 'accounts/change_profile.html'

    def get(self, request, *args, **kwargs):
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('change_profile')
        else:
            messages.error(request, 'Please correct the error below.')


class ViewProfileView(View):
    template_name = 'accounts/view_profile.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', request.user.username)
        user = get_object_or_404(User, username=username)

        return render(request, self.template_name, {
            'user': user,
            'following': Follow.objects.follows(request.user, user),
            'image_list': ImageConversion.objects.filter(author=user),
            'follower_list': Follow.objects.followers(user)
        })


class FollowCreate(LoginRequiredMixin, View):
    def post(self, request):
        Follow.objects.add_follower(request.user,
                                    get_object_or_404(User, username=request.POST['username']))
        return redirect(request.POST['next'])


class FollowDelete(LoginRequiredMixin, View):
    def post(self, request):
        Follow.objects.remove_follower(request.user,
                                       get_object_or_404(User, username=request.POST['username']))
        return redirect(request.POST['next'])
