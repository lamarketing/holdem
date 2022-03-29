from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('cards.urls')),
    path('api/v1/', include('dev.urls')),
]
