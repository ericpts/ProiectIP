from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from images import views

urlpatterns = [
    url(r'^delete/(?P<pk>\d+)/$',
        views.ImageDelete.as_view(),
        name='delete'),
    url(r'^upload/$', views.ImageCreate.as_view(), name='upload'),
    url(r'^album/(?P<username>[\w\+\.\-_]{0,50})/$',
        views.AlbumView.as_view(),
        name='album'),
    url(r'^album/$', views.AlbumView.as_view(), name='my_album'),
    url(r'^latest/$', views.LatestView.as_view(), name='latest'),

    url(r'^image/(?P<pk>\d+)/$',
        views.ImageDetailView.as_view(),
        name='image_detail'),

    url(r'^image_rate/(?P<pk>\d+)/$',
        views.ImageRateView.as_view(),
        name='image_rate'),
    url(r'^image_download/(?P<pk>\d+)/$',
        views.ImageDownload.as_view(),
        name='image_download')
]
