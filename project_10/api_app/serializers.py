from .models import CustomUser, Contributor, Project, Issue, Comment
from rest_framework import serializers

class CreateContributor(serializers.Serializer):
    class Meta:
        fields = ['email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'tag', 'priority','assignee_user_id']

        extra_kwargs = {
            'created_time': { 'read_only': True },
            'project_id': { 'read_only': True },
            'author_user_id': { 'read_only': True },
            }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description']

        extra_kwargs = {
            'created_time': { 'read_only': True },
            'issue_id': { 'read_only': True },
            'author_user_id': { 'read_only': True },
            }
