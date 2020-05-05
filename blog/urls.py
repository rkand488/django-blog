from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from blog import views
from blog.models import Post

urlpatterns = [
    path("", views.home, name="home"),
    re_path(r'^search/$', views.search, name="search"),
    re_path(r"^(?P<slug>[-\w]+)/$", views.view_post, name="view_post"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path("post", views.post, name="post"),
    # path("post/<id>", views.add_post, name="edit_post"),
    # path("add-post", views.add_post, name="add_post"),
    re_path(
        r'^archive/month/(?P<year>\d+)/(?P<month>\w+)$',
        views.PostMonthArchiveView.as_view(),
        name='archive_month',
    ),
    re_path(
        r'^archive/week/(?P<year>\d+)/(?P<week>\d+)$',
        views.PostWeekArchiveView.as_view(),
        name='archive_week',
    ),
]