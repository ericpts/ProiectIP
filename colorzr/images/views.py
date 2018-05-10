import random
import uuid

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from friendship.models import Follow
from django.http import HttpResponse

from . import forms
from . import models

from social.models import Rating, Comment
from .forms import CommentAddForm


class ImageCreate(LoginRequiredMixin, generic.FormView):
    form_class = forms.ImageAddForm
    success_url = reverse_lazy('my_album')
    template_name = 'images/upload-image.html'

    def form_valid(self, form):
        original_image = form.cleaned_data['original_image']
        title = form.cleaned_data['title']

        bw, color = models.ImageConversion.convert(original_image)
        # Random names for conversions
        name = str(uuid.uuid4()) + '.jpg'

        model_image = models.ImageConversion()

        model_image.title = title
        model_image.author = self.request.user
        model_image.original_image.save(name, original_image)
        model_image.bw_image.save(name, bw)
        model_image.color_image.save(name, color)

        model_image.save()

        return super().form_valid(form)


class ImageDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.ImageConversion
    success_url = reverse_lazy('my_album')

    def get_queryset(self):
        return models.ImageConversion.objects.filter(author__exact=self.request.user)


class AlbumView(LoginRequiredMixin, generic.ListView):
    template_name = 'images/album.html'
    model = models.ImageConversion
    context_object_name = 'image_list'
    paginate_by = 20
    author = None

    def get_context_data(self, **kwargs):
        kwargs['author'] = self.author
        kwargs['is_own'] = self.author == self.request.user
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username', request.user.username)
        self.author = get_object_or_404(User, username=username)

        return super(AlbumView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return models.ImageConversion.objects.filter(author__exact=self.author)


class LatestView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'images/latest.html'
    model = models.ImageConversion
    context_object_name = 'image_list'

    def get_context_data(self, **kwargs):
        kwargs["new_images"] = models.ImageConversion.objects.order_by('-id')[:9]
        kwargs["following_images"] = models.ImageConversion.objects\
            .filter(author__in=Follow.objects.following(self.request.user))\
            .order_by('-id')[:9]
        kwargs["trending_images"] = models.ImageConversion.objects\
            .annotate(num_ratings=Count('rating')+Count('comment'))\
            .order_by('-num_ratings')[:9]
        kwargs["random_images"] = models.ImageConversion.objects.order_by('?')[:9]

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return models.ImageConversion.objects.order_by('-created')


class ImageDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'images/detail.html'
    model = models.ImageConversion
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        kwargs['comment_form'] = forms.CommentAddForm

        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.CommentAddForm(request.POST)
        if form.is_valid():
            image_pk = self.kwargs['pk']
            image = get_object_or_404(models.ImageConversion, pk=image_pk)

            Comment.objects.create(
                author=request.user,
                image=image,
                text=form.cleaned_data['text']
            )
            messages.success(request, 'Comment posted successfully!')
        return redirect(request.POST['next'])


class ImageRateView(generic.View):
    def post(self, request, *args, **kwargs):
        image_pk = kwargs['pk']
        image = get_object_or_404(
                models.ImageConversion, pk=image_pk)
        rating = int(request.POST['rating'])
        Rating.objects.update_or_create(
                author=request.user,
                image=image,
                defaults={'rating': rating},
        )
        return HttpResponse(status=204)