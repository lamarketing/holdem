from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', views.obtain_auth_token),
    path('api/v1/', include('cards.urls')),
    path('api/v1/', include('tournaments.urls')),
]
