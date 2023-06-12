from django.contrib import admin
from .models import (
	Answer,
	Enrollment,
	QuizProgress,
	TopicProgress,
)

class AnswerAdminTable(admin.ModelAdmin):
	list_display = ('quiz', 'question', 'student', 'answer_text', 'hint_used', 'is_correct', 'time_taken', 'attempt')
	list_filter = ('hint_used', 'is_correct')

class QuizProgressAdminTablel(admin.ModelAdmin):
	list_display = ('pk', 'enrollment', 'quiz', 'score', 'is_completed')
	list_filter = ('is_completed',)

class TopicProgressAdminTablel(admin.ModelAdmin):
	list_display = ('pk', 'enrollment', 'topic', 'is_completed')
	list_filter = ('is_completed',)

admin.site.register(Answer, AnswerAdminTable)
admin.site.register(Enrollment)
admin.site.register(QuizProgress, QuizProgressAdminTablel)
admin.site.register(TopicProgress, TopicProgressAdminTablel)