from django.contrib import admin
from django.urls import include, path
from api_app import views

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('', include('api_app.urls')),
    path('admin/', admin.site.urls),
    path('login/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),
]
