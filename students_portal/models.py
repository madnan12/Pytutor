from django.db import models
from users.models import CustomUser
from teachers_portal.models import Course, Topic, Quiz, QuizQuestion

Enrollment_Status = [
	("Enrolled", "Enrolled"),
	("In Progress", "In Progress"),
	("Completed", "Completed"),
	("Dropped", "Dropped"),
	("Failed", "Failed"),
]

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', verbose_name='Student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    total_topics = models.IntegerField(verbose_name='Total Topics')
    topics_progress = models.ManyToManyField(Topic, through='TopicProgress')
    total_quizes = models.IntegerField(verbose_name='Total Quizes')
    quizzes_progress = models.ManyToManyField(Quiz, through='QuizProgress')
    grade = models.CharField(max_length=1, null=True, blank=True, verbose_name='Grade')
    enroll_date = models.DateTimeField(auto_now_add=True, verbose_name='Enrollment Date')
    status = models.CharField(max_length=15, choices=Enrollment_Status, verbose_name='Status')
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name='Completion Date')
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    
    def __str__(self):
    	return f"{self.pk}"
 
    def get_topics_progress_percent(self):
        total_topics = self.total_topics
        if total_topics > 0:
            completed_topics = self.topics_progress.through.objects.filter(enrollment=self, is_completed=True).count()
            progress_percent = completed_topics / total_topics * 100
            return progress_percent
        else:
            return 0
        
    def get_quizzes_progress_percent(self):
        total_quizes = self.total_quizes
        if total_quizes > 0:
            completed_quizzes = self.quizzes_progress.through.objects.filter(enrollment=self, is_completed=True).count()
            progress_percent = completed_quizzes / total_quizes * 100
            return progress_percent
        else:
            return 0


    def get_enrollment_quizes(self):
        quizes = QuizProgress.objects.filter(enrollment=self)
        return quizes


    class Meta:
    	verbose_name_plural = 'Enrollments'
    	ordering = ['pk']

class TopicProgress(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Topic')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, verbose_name='Enrollment')
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='Completed Date')
    feedback = models.CharField(max_length=255, blank=True, verbose_name='Teachers Feedback')

    def __str__(self):
    	return f"{self.pk}"

    class Meta:
    	verbose_name_plural = 'Students Topic Progress'
    	ordering = ['pk']

class QuizProgress(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, verbose_name='Enrollment')
    score = models.IntegerField(null=True, blank=True, verbose_name='Score')
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='Completed Date')
    feedback = models.CharField(max_length=255, blank=True, verbose_name='Teachers Feedback')

    def __str__(self):
    	return f"{self.pk}"

    class Meta:
    	verbose_name_plural = 'Students Quiz Progress'
    	ordering = ['pk']

class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, verbose_name='Question')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Student')
    answer_text = models.TextField(verbose_name='Answer')
    is_correct = models.BooleanField(verbose_name='Is Correct')
    explanation = models.TextField(blank=True, null=True, verbose_name='Explanation')
    feedback = models.TextField(blank=True, null=True, verbose_name='Feedback')
    time_taken = models.FloatField(blank=True, null=True, verbose_name='Time Taken')
    attempt = models.IntegerField(default=1, verbose_name='Attempt')
    hint_used = models.BooleanField(default=False, verbose_name='Hint Used')

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name_plural = 'Answers'
        ordering = ['pk']