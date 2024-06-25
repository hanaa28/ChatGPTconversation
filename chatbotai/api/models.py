from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thread by {self.user.username} at {self.created_at}'

class Message(models.Model):
    _input = models.TextField()
    _output = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.user.username} in thread {self.thread.id}'

