from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your models here.

class ValidateOnSaveMixin(object):

    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update,
                                              **kwargs)

def validate_length(value):
    if len(value) < 3:
        raise ValidationError('Length should be between 3 and 40')

def validate_gender(value):
    if value == 'M' or value == 'F':
        pass
    else:
        raise ValidationError('Gender should be either "M" or "F"')

class Candidate(ValidateOnSaveMixin, models.Model):

    email = models.EmailField(validators = [validate_email])
    first_name = models.CharField(validators = [validate_length], max_length = 40)
    last_name = models.CharField(validators = [validate_length], max_length = 40)
    city = models.CharField(validators = [validate_length], max_length = 40)
    country = models.CharField(validators = [validate_length], max_length = 40)
    gender = models.CharField(validators = [validate_gender], max_length = 1)

class WorkExperience(models.Model):

    user = models.ForeignKey(Candidate)
    experienced = models.BooleanField()
    years_of_experience = models.SmallIntegerField()
    months_of_experience = models.SmallIntegerField()
