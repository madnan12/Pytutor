from pytutor.utils import unique_slug_generator
from django.db.models.signals import pre_save
from .models import Course, Topic, Quiz

# generates slug value according to the instance name on save, update
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Course)
pre_save.connect(slug_generator, sender=Topic)
pre_save.connect(slug_generator, sender=Quiz)