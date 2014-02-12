from django.db import models

# Create your models here.

class Candidate(models.Model):

    email = models.EmailField(blank = False, null = False)
    first_name = models.CharField(max_length = 30, blank = False)
    last_name = models.CharField(max_length = 50, blank = False)
    city = models.CharField(max_length = 60, blank = False)
    country = models.CharField(max_length = 50, blank = False)
    gender = models.CharField(max_length = 1, blank = False)

class WorkExperience(models.Model):

    user = models.ForeignKey(Candidate)
    experienced = models.BooleanField()
    years_of_experience = models.SmallIntegerField()
    months_of_experience = models.SmallIntegerField()


