# Generated by Django 4.1.7 on 2023-05-02 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_portal', '0007_quizquestion_correct_answer_quizquestion_hint_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='ordering',
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions_order',
            field=models.CharField(choices=[('Creation', 'Creation'), ('Random', 'Random')], default=1, max_length=10, verbose_name='Questions Sorting Order'),
            preserve_default=False,
        ),
    ]
