from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from images import views

urlpatterns = [
    url(r'^$', views.ImageList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
    url(r'upload-image', views.ImageAddView.as_view()),
]
