from django.urls import include, path
from rest_framework_nested import routers

from . import views

nested_router = routers.SimpleRouter()
nested_router.register(r'projects', views.ProjectViewSet, basename='project')
nested_router.register(r'issues', views.IssueViewSet, basename='issue')

projects_router = routers.NestedSimpleRouter(nested_router, r'projects',
                                            lookup='project'
                                            )
projects_router.register(r'users', views.ViewContributors,
                        basename='project-users'
                        )
projects_router.register(r'issues', views.IssueViewSet,
                        basename='project-issues'
                        )

issues_router = routers.NestedSimpleRouter(projects_router, r'issues',
                                        lookup='issue'
                                        )
issues_router.register(r'comments', views.CommentViewSet,
                    basename='comments'
                    )

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('', include(nested_router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls))
]
