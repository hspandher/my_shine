from django.db import models

# Create your models here.

class Candidate(models.Model):

    email = models.EmailField(blank = False)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 50)
    city = models.CharField(max_length = 60)
    country = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 1)

class WorkExperience(models.Model):

    user = models.ForeignKey(Candidate)
    experienced = models.BooleanField()
    years_of_experience = models.SmallIntegerField()
    months_of_experience = models.SmallIntegerField()


