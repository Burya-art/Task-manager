from django.contrib import admin
from django.urls import include, path

from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home_redirect, name='home'),
    path('', include('tasks.urls')),
]
