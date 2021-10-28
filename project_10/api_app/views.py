from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import CustomUser, Contributor, Project, Issue, Comment
from .permissions import IsForbidden, IsAuthor
from .serializers import CreateUserSerializer, UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, CreateContributor


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
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'delete':
            permission_classes = [IsAuthor]
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


class ViewContributors(viewsets.ModelViewSet):
    """Show the contributors of a given project."""
    def get_permissions(self):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = self.request.user
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif user.is_author(project):
            if self.action == 'create' or self.action == 'delete':
                permission_classes = [IsAuthor]
        else:
            permission_classes = [IsForbidden]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        if self.action == 'create':
            return CreateContributor

    def get_queryset(self):
        contrib_profiles = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        users_id = [contributor.user_id for contributor in contrib_profiles]
        list_users = CustomUser.objects.filter(id__in=users_id)

        return list_users

    def perform_destroy(self, instance):
        user = instance
        contrib_profile = Contributor.objects.get(project_id=self.kwargs['project_pk'],
                                                user_id=user.id
                                                )
        contrib_profile.delete()

    def perform_create(self, serializer):
        email = serializer.data['email']
        user = CustomUser.objects.get(email=email)
        project = Project.objects.get(id=self.kwargs['project_pk'])
        already_exists = Contributor.objects.filter(project_id=project.id,
                                                    user_id=user.id
                                                    )
        if already_exists:
            return user
        else:
            new_contrib = project.add_contrib(project.id, user.id)
            return new_contrib


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk']).order_by('-created_time')

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'],
                        author_user_id=self.request.user,
                        assignee_user_id=self.request.user
                        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk']).order_by('-created_time')

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(issue_id=issue, author_user_id=self.request.user)
