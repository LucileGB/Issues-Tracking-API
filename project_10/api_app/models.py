from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, first_name, last_name, password):
        if not email:
            raise ValueError('Veuillez entrer votre adresse e-mail.')
        if not first_name:
            raise ValueError('Veuillez entrer votre prénom.')
        if not last_name:
            raise ValueError('Veuillez entrer votre nom de famille.')

        user = self.model(email=self.normalize_email(email),
                        first_name=first_name,
                        last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(email=self.normalize_email(email),
                        first_name=first_name, last_name=last_name,
                        **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Contributor(models.Model):
    AUTHOR = "Auteur"
    RESPONSABLE = "Responsable"
    CONTRIBUTOR = "Contributeur"
#NOTE : Choisir choix de permissions !!
    PERMISSION_CHOICES = (
        (AUTHOR, 'Auteur'), (CONTRIBUTOR, 'Contributeur'), (RESPONSABLE, 'Responsable')
        )

    user_id = models.IntegerField('user id')
    project_id = models.IntegerField('project id')
    permission = models.CharField(choices=PERMISSION_CHOICES, max_length=20)
    role = models.CharField('role', max_length=100)

    def __str__(self):
        return self.user_id


class Project(models.Model):
    BACKEND = 'Back-End'
    FRONTEND = 'Front-End'
    ANDROID = 'Android'
    TYPE_CHOICES = (
        (BACKEND, 'Back-End'), (FRONTEND, 'Front-End'), (ANDROID, 'Android')
        )

    project_id = models.IntegerField('project id')
    title = models.CharField('title', max_length=50)
    description = models.CharField('description', max_length=250)
    type = models.CharField('type', choices=TYPE_CHOICES, max_length=20)
#NOTE : changer on_delete
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Issue(models.Model):
    LOW = 'Basse'
    AVERAGE = 'Moyenne'
    HIGH = 'Haute'
    BUG = 'Bug'
    IMPROVEMENT = 'Amelioration'
    TASK = 'Tache'
    TODO = 'A faire'
    ONGOING = 'En cours'
    FINISHED = 'Termine'

    PRIORITY_CHOICES = (
        (LOW, 'Basse'), (AVERAGE, 'Moyenne'), (HIGH, 'Haute')
        )
    TAG_CHOICES = (
        (BUG, 'Bug'), (IMPROVEMENT, 'Amélioration'), (TASK, 'Tâche')
    )
    STATUS_CHOICES = (
        (TODO, 'A faire'), (ONGOING, 'En cours'), (FINISHED, 'Terminé')
    )

    title = models.CharField('title', max_length=50)
    description = models.CharField('description', max_length=250)
    tag = models.CharField('tag', choices=TAG_CHOICES, max_length=50)
    priority = models.CharField('priority', choices=PRIORITY_CHOICES, max_length=50)
    project_id = models.IntegerField('project id')
    status = models.CharField('status', choices=TAG_CHOICES, max_length=50)
#NOTE : changer on_delete
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
#NOTE : moyen d'assigner l'auteur directement ? Sur une fonction, probablement.
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.IntegerField("comment id")
    description = models.CharField('description', max_length=250)
#NOTE : changer on_delete
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_id
