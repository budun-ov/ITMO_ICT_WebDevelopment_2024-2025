from django.contrib import admin
from .models import Racer, Race, Result, Comment, RaceRegistration

@admin.register(Racer)
class RacerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team_name', 'class_type')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'race_class')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'racer', 'result_time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('race', 'commenter', 'comment_type', 'created_at')

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'racer', 'registration_date')