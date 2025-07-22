from django.db import models
from users.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import User

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=100)
    round_type = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)  # optional: for gamification
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_role} - {self.round_type}"

class InterviewQuestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True)
    job_role = models.CharField(max_length=100)
    round = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.round} - {self.job_role}"
    


