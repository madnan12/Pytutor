from django.db import models
from django.urls import reverse
from users.models import CustomUser
from administration.models import Subject

Field_Types = (
    ('text', 'text'),
    ('number', 'number'),
    ('radio', 'radio'),
    ('checkbox', 'checkbox'),
    ('Drop Down', 'Drop Down'),
    ('Code', 'Code'),
)

Questions_Order = (
    ('Creation','Creation'),
    ('Random', 'Random')
)

class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Title')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Subject')
    description = models.TextField(verbose_name='Description')
    slug = models.CharField(max_length=260, unique=True, blank=True, null=True, verbose_name='Slug')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Created By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated on')

    def __str__(self):
    	return f"{self.title}"

    def get_absolute_list_url(self):
        return reverse('teachers_portal:course-list')

    def get_absolute_edit_url(self):
        return reverse('teachers_portal:update-course', kwargs={'slug': self.slug })

    def get_absolute_delete_url(self):
        return reverse('teachers_portal:delete-course', kwargs={'slug': self.slug })

    def get_topics_count(self):
        return Topic.objects.filter(course=self).count()

    def get_topics_list(self):
        return Topic.objects.filter(course=self)

    def get_quizes_count(self):
        quiz_count = 0
        for topic in Topic.objects.filter(course=self):
            quiz_count += topic.get_quizes_count()
        return quiz_count

    class Meta:
    	verbose_name_plural = 'Courses'
    	ordering = ['pk']

class Topic(models.Model):
    title = models.CharField(max_length=250, verbose_name='Title')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    description = models.TextField()
    slug = models.CharField(max_length=260, unique=True, blank=True, null=True, verbose_name='Slug')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Created By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated on')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_list_url(self):
        return reverse('teachers_portal:topic-list')

    def get_absolute_edit_url(self):
        return reverse('teachers_portal:update-topic', kwargs={'slug': self.slug })

    def get_absolute_delete_url(self):
        return reverse('teachers_portal:delete-topic', kwargs={'slug': self.slug })

    def get_quizes_list(self):
        return Quiz.objects.filter(topic=self)

    def get_quizes_count(self):
        return Quiz.objects.filter(topic=self).count()

    class Meta:
        verbose_name_plural = 'Topics'
        ordering = ['pk']

class Quiz(models.Model):
    title = models.CharField(max_length=250, verbose_name='Title')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Course')
    description = models.TextField()
    questions_order = models.CharField(max_length=10, choices=Questions_Order, verbose_name='Questions Sorting Order')
    slug = models.CharField(max_length=260, unique=True, blank=True, null=True, verbose_name='Slug')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Created By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated on')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_list_url(self):
        return reverse('teachers_portal:quiz-list')

    def get_absolute_edit_url(self):
        return reverse('teachers_portal:update-quiz', kwargs={'slug': self.slug })

    def get_absolute_delete_url(self):
        return reverse('teachers_portal:delete-quiz', kwargs={'slug': self.slug })

    def get_questions_list(self):
        return QuizQuestion.objects.filter(quiz=self)

    def get_question_count(self):
        return QuizQuestion.objects.filter(quiz=self).count()

    class Meta:
        verbose_name_plural = 'Quizes'
        ordering = ['pk']

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz')
    question = models.CharField(max_length=500, verbose_name='Question')
    question_type = models.CharField(max_length=35, choices=Field_Types, verbose_name='Question Type')
    correct_answer = models.CharField(max_length=250, null=True, blank=True, verbose_name='Question Answer')
    hint_text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Hint')
    is_required = models.BooleanField(default=False, verbose_name='Is Required')
    slug = models.CharField(max_length=260, unique=True, blank=True, null=True, verbose_name='Slug')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Created By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated on')

    def __str__(self):
        return f"{self.question}"

    def get_question_choices(self):
        return QuestionChoices.objects.filter(question=self)

    class Meta:
        verbose_name_plural = 'Quiz Questions'
        ordering = ['pk']

class QuestionChoices(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, verbose_name='Question')
    choice_statement = models.CharField(max_length=250, verbose_name='Choice Option')

    def __str__(self):
        return f"{self.choice_statement}"

    class Meta:
        verbose_name_plural = 'Question Choices'
        ordering = ['pk']

class TeacherEnrollment(models.Model):
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_enrollment')
    enrolled_students = models.ManyToManyField(CustomUser, related_name='teacher_enrollments')

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name_plural = 'Teacher Enrollments'
        ordering = ['pk']
