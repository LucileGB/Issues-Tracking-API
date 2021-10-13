from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api_app import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'contributors', views.ContributorViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', views.HelloView.as_view(), name ='hello'),
]
