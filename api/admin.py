from django.contrib import admin
from .models import Conversation, SystemPrompt
# Register your models here.
admin.site.register(Conversation)
admin.site.register(SystemPrompt)
