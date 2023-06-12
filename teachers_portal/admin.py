from django.contrib import admin
from .models import Course, Topic, Quiz, QuizQuestion, QuestionChoices, TeacherEnrollment

class CourseAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'title', 'subject', 'created_by')

class TopicAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'title', 'course', 'created_by')

class QuizAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'title', 'topic', 'created_by', 'slug')

class QuizQuestionAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'question', 'quiz', 'correct_answer', 'created_by')

class QuestionChoicesAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'choice_statement', 'question', 'quiz')

class TeacherEnrollmentAdminTable(admin.ModelAdmin):
	list_display = ('pk', 'teacher')

admin.site.register(Course, CourseAdminTable)
admin.site.register(Topic, TopicAdminTable)
admin.site.register(Quiz, QuizAdminTable)
admin.site.register(QuizQuestion, QuizQuestionAdminTable)
admin.site.register(QuestionChoices, QuestionChoicesAdminTable)
admin.site.register(TeacherEnrollment, TeacherEnrollmentAdminTable)