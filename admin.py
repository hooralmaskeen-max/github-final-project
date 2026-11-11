from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import Question, Choice, Submission, Lesson

class ChoiceInline(TabularInline):
    model = Choice
    extra = 1

class QuestionInline(TabularInline):
    model = Question
    extra = 1

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline]
    search_fields = ['text']
    list_display = ['text', 'created_at']

@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title']

@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ['question', 'selected_choice', 'submitted_at']
