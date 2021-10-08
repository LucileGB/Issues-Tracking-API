#from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import CustomUser, Contributor, Project, Issue, Comment
from .serializers import UserSerializer, ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-email')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by('-user_id')
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_time')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_time')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
