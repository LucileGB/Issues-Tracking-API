from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, generics, status

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import CustomUser, Contributor, Project, Issue, Comment
from .permissions import IsContributor, IsAuthor, ContributorList
from .serializers import CreateUserSerializer, UserSerializer, ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, CreateContributor


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsContributor]
        elif self.action == 'update' or self.action == 'delete':
            permission_classes = [IsAuthor]
#NOTE: or IsStaff?
        else:
            permission_classes = [IsAuthor]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.request.user.contributes_in()

        return queryset

    def perform_create(self, serializer):
        project = serializer.save(author_user_id=self.request.user)
        project.create_author()

    def perform_destroy(self, instance):
        project = instance
        project.delete_all_contrib()
        project.delete_all_issues()
        project.delete()

    @action(detail=True, methods=['get', 'post', 'delete'])
    def users(self, request, pk=None):
        if request.method == 'GET':
            contrib_profiles = Contributor.objects.filter(project_id=pk)
            users_id = [contributor.user_id for contributor in contrib_profiles]
            list_users = CustomUser.objects.filter(id__in=users_id)
            page = self.paginate_queryset(list_users)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.UserSerializer(list_users, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = self.UserSerializer(list_users, many=True)
            return Response(serializer.data)


class ViewContributors(viewsets.ModelViewSet):
    """Show the contributors of a given project."""
    permission_classes = [ContributorList]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action == 'post':
            return CreateContributor

    def get_queryset(self):
        contrib_profiles = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        users_id = [contributor.user_id for contributor in contrib_profiles]
        list_users = CustomUser.objects.filter(id__in=users_id)

        return list_users

    def perform_destroy(self, instance):
        user = instance
        contrib_profile = Contributor.objects.get(project_id=self.kwargs['project_pk'], user_id=instance.id)
        contrib_profile.delete()

    def perform_create(self, serializer):
        email = serializer['email']
        user = CustomUser.objects.get(email=email)
        new_contrib = Project.add_contrib(project_id=self.kwargs['project_pk'], user_id=user.id)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk']).order_by('-created_time')

    def perform_create(self, serializer):
        issue = serializer.save(project_id=self.kwargs['project_pk'], author_user_id=self.request.user,
                                assignee_user_id=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk']).order_by('-created_time')

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        comment = serializer.save(issue_id=issue, author_user_id=self.request.user)
