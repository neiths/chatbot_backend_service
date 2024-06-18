from rest_framework import serializers
from api.models import Conversation, SystemPrompt

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"

class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = "__all__"