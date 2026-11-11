from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import User
from .models import Question, Choice, Submission, Lesson, Course, Enrollment, UserProfile

class ChoiceInline(TabularInline):
    model = Choice
    extra = 1

class QuestionInline(TabularInline):
    model = Question
    extra = 1

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    inlines = [ChoiceInline]
    search_fields = ['question_text']  
    list_display = ['question_text', 'created_at'] 

@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title']

@admin.register(Submission)
class SubmissionAdmin(ModelAdmin):
    list_display = ['enrollment', 'submitted_at']  

@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ['title']

@admin.register(Enrollment)
class EnrollmentAdmin(ModelAdmin):
    list_display = ['user', 'course']

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ['user']
