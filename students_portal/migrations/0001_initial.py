# Generated by Django 4.1.7 on 2023-04-15 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers_portal', '0006_questionchoices_quiz_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_topics', models.IntegerField(verbose_name='Total Topics')),
                ('total_quizes', models.IntegerField(verbose_name='Total Quizes')),
                ('grade', models.CharField(blank=True, max_length=1, null=True, verbose_name='Grade')),
                ('enroll_date', models.DateTimeField(auto_now_add=True, verbose_name='Enrollment Date')),
                ('status', models.CharField(choices=[('Enrolled', 'Enrolled'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Dropped', 'Dropped'), ('Failed', 'Failed')], max_length=15, verbose_name='Status')),
                ('completion_date', models.DateTimeField(blank=True, null=True, verbose_name='Completion Date')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_portal.course', verbose_name='Course')),
            ],
            options={
                'verbose_name_plural': 'Enrollments',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='TopicProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_date', models.DateTimeField(blank=True, null=True, verbose_name='Completed Date')),
                ('feedback', models.CharField(blank=True, max_length=255, verbose_name='Teachers Feedback')),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students_portal.enrollment', verbose_name='Enrollment')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_portal.topic', verbose_name='Topic')),
            ],
            options={
                'verbose_name_plural': 'Students Topic Progress',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='QuizProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='Score')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('completed_date', models.DateTimeField(blank=True, null=True, verbose_name='Completed Date')),
                ('feedback', models.CharField(blank=True, max_length=255, verbose_name='Teachers Feedback')),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students_portal.enrollment', verbose_name='Enrollment')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_portal.quiz', verbose_name='Quiz')),
            ],
            options={
                'verbose_name_plural': 'Students Quiz Progress',
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='enrollment',
            name='quizzes_progress',
            field=models.ManyToManyField(through='students_portal.QuizProgress', to='teachers_portal.quiz'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='topics_progress',
            field=models.ManyToManyField(through='students_portal.TopicProgress', to='teachers_portal.topic'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(verbose_name='Answer')),
                ('is_correct', models.BooleanField(verbose_name='Is Correct')),
                ('explanation', models.TextField(blank=True, null=True, verbose_name='Explanation')),
                ('feedback', models.TextField(blank=True, null=True, verbose_name='Feedback')),
                ('time_taken', models.FloatField(blank=True, null=True, verbose_name='Time Taken')),
                ('attempt', models.IntegerField(default=1, verbose_name='Attempt')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_portal.quizquestion', verbose_name='Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers_portal.quiz', verbose_name='Quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name_plural': 'Answers',
                'ordering': ['pk'],
            },
        ),
    ]
