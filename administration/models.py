from django.db import models
from users.models import CustomUser
from django.urls import reverse

class Subject(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True, verbose_name='Slug')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Created By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated on')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_list_url(self):
    	return reverse('administration:subject-list')

    def get_courses_count(self):
        return Course.objects.filter(subject=self).count()

    class Meta:
    	verbose_name_plural = 'Subjects'
    	ordering = ['pk']