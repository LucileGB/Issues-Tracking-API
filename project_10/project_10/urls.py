from django.contrib import admin
from django.urls import include, path
from api_app import views

urlpatterns = [
    path('', include('api_app.urls')),
    path('admin/', admin.site.urls),
    path('authenticate/', include('rest_framework.urls', namespace='rest_framework')),
]
