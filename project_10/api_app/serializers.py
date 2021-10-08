from .models import CustomUser, Contributor, Project, Issue, Comment
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'user_id', 'first_name', 'last_name', 'email']


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ['url', 'user_id', 'project_id', 'permission', 'role']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'title', 'description', 'type', 'author_user_id']

        extra_kwargs = {
            'project_id': { 'read_only': True },
            }


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ['url', 'title', 'description', 'tag', 'priority','assignee_user_id']

        extra_kwargs = {
            'created_time': { 'read_only': True },
            'project_id': { 'read_only': True },
            'author_user_id': { 'read_only': True },
            }


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['url', 'comment_id', 'description']

        extra_kwargs = {
            'created_time': { 'read_only': True },
            'issue_id': { 'read_only': True },
            'author_user_id': { 'read_only': True },
            }
