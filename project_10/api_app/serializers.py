from rest_framework import serializers

from .models import CustomUser, Contributor, Project, Issue, Comment


class CreateContributor(serializers.Serializer):
    """Is used only to stock an email adress."""
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

    extra_kwargs = {
        'id': {'read_only': True},
        }


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description']

        extra_kwargs = {
            'id': {'read_only': True},
            'created_time': {'read_only': True},
            'issue_id': {'read_only': True},
            'author_user_id': {'read_only': True},
            }


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission']

        extra_kwargs = {
            'id': {'read_only': True},
            'project_id': {'read_only': True},
            'permission': {'read_only': True},
            }


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag',
                'priority', 'assignee_user_id']

        extra_kwargs = {
            'id': {'read_only': True},
            'created_time': {'read_only': True},
            'project_id': {'read_only': True},
            'author_user_id': {'read_only': True},
            }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    extra_kwargs = {
        'id': {'read_only': True},
        }
