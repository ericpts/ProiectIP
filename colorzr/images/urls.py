from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from images import views

urlpatterns = [
    url(r'^images/$', views.ImageList.as_view()),
    url(r'^images/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)