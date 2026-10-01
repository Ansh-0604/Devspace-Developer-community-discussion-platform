from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, default="Other")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      bio = models.TextField(blank=True)

      def __str__(self):
        return self.user.username




class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField()

    tech_stack = models.CharField(max_length=300, blank=True)
    github_link = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('planning', 'Planning'),
            ('building', 'Building'),
            ('completed', 'Completed'),
            ('paused', 'Paused'),
        ],
        default='planning'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DevLog(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='devlogs'
    )

    title = models.CharField(max_length=200)

    log_type = models.CharField(
        max_length=20,
        choices=[
            ('build', 'Build'),
            ('bug', 'Bug'),
            ('decision', 'Decision'),
            ('learning', 'Learning'),
            ('milestone', 'Milestone'),
        ],
        default='build'
    )

    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

