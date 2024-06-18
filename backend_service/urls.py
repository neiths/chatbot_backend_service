"""
URL configuration for backend_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import generics
from api.views import conversationSerializer_list_create, conversationSerializer_retrieve_update_destroy, \
systemPromptSerializer_list_create, systemPromptSerializer_retrieve_update_destroy, answer_message


from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API for chatbot",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("conversation/", conversationSerializer_list_create, name="conversation-list-create"),
    path("conversation/<int:pk>/", conversationSerializer_retrieve_update_destroy, name="conversation-retrieve-update-destroy"),
    path("prompt/", systemPromptSerializer_list_create, name="system-prompt-list-create"),
    path("prompt/<int:pk>/", systemPromptSerializer_retrieve_update_destroy, name="system-prompt-retrieve-update-destroy"),
    path("answer/", answer_message, name="answer-message"),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
