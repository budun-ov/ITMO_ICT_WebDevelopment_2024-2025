from django.urls import path
from .views import WarriorAPIView, ProfessionCreateView, SkillAPIView, SkillCreateView, \
                   WarriorDetailView, WarriorSkillsListView, WarriorProfessionListView

urlpatterns = [
    path('warriors/', WarriorAPIView.as_view()),
    path('warriors/<int:pk>', WarriorDetailView.as_view()),
    path('warriors/skills/', WarriorSkillsListView.as_view()),
    path('warriors/professions/', WarriorProfessionListView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/create/', SkillCreateView.as_view()),
    path('profession/create/', ProfessionCreateView.as_view()),
    ]