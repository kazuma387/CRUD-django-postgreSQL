from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('repreStudy/', include('repreStudy.urls')),
    path('', views.index , name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
]
