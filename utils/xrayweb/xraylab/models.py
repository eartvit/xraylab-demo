from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class XRayData(models.Model):
    test_date = models.DateTimeField(default=timezone.now)  # Don't put the paranthesis, just the function name
    name = models.CharField(max_length=100)  # Patient's name
    risk = models.FloatField()
    notes = models.TextField(blank=True, null=True)  #The comment added by the doctor.
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_name = models.ImageField(blank=True, null=True, upload_to='', max_length=255)
    model_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('xraylab-details-update', kwargs={'pk': self.pk})
