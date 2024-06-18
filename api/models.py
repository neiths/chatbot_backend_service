from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Conversation(models.Model):
    user_id = models.AutoField(primary_key=True)
    expert_name = models.CharField(max_length=255)
    gpt_model = models.CharField(max_length=255)
    chat_history = ArrayField(models.JSONField(), default=list)
    #created_at = models.DateTimeField(auto_now_add=True)
    meta_data = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.expert_name} - {self.gpt_model}"
    

class SystemPrompt(models.Model):
    expert_id = models.AutoField(primary_key=True)
    expert_name = models.CharField(max_length=255, unique=True)
    prompt = models.TextField()

    def __str__(self):
        return f"{self.expert_id} - {self.expert_name}"