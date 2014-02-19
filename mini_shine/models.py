from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import datetime
import re
# Create your models here.

class ValidateOnSaveMixin(object):

    # pass
    def save(self, force_insert=False, force_update=False, **kwargs):
        if not (force_insert or force_update):
            self.full_clean()
        super(ValidateOnSaveMixin, self).save(force_insert, force_update,
                                              **kwargs)
def validate_email_uniqueness(value):
    if Candidate.objects.filter(email = value):
        raise ValidationError('Email already exists in database')

def validate_length(value):
    if len(value) < 3:
        raise ValidationError('Length should be between 3 and 40')

def validate_gender(value):
    if value == 'M' or value == 'F':
        pass
    else:
        raise ValidationError('Gender should be either "M" or "F"')

def validate_mobile_number(value):
    valid = re.match(r'^\d{9,15}$', value)
    if not valid:
        raise ValidationError('Not a valid mobile Number')

def validate_years(value):
    if value != int(value) or value >= 70 or value < 0:
        raise ValidationError('Invalid value for the year')

def validate_months(value):
    if value != int(value) or value > 12 or value < 0:
        raise ValidationError('Invalid value for months')

def validate_highest_qualifications(value):
    if value == '10' or value == '10+2' or value == 'Graduation' or value == 'Post Graduation' or value == 'Diploma/Vocational Courses':
        pass
    else:
        raise ValidationError('Invalid Highest Qualification')

class Candidate(ValidateOnSaveMixin, models.Model):

    email = models.EmailField(validators = [validate_email], unique = True)
    first_name = models.CharField(validators = [validate_length], max_length = 40)
    last_name = models.CharField(validators = [validate_length], max_length = 40)
    city = models.CharField(validators = [validate_length], max_length = 40)
    country = models.CharField(validators = [validate_length], max_length = 40)
    gender = models.CharField(validators = [validate_gender], max_length = 1)
    password = models.CharField(validators = [validate_length], max_length = 40)
    mobile_number = models.CharField(validators = [validate_mobile_number], max_length = 15)

    # Added due to stupid bug with custom models in django
    last_login = models.DateTimeField(default=datetime.datetime.now)

class WorkExperience(ValidateOnSaveMixin, models.Model):

    candidate = models.ForeignKey(Candidate)
    is_experienced = models.BooleanField()
    years_of_experience = models.SmallIntegerField(validators = [validate_years])
    months_of_experience = models.SmallIntegerField(validators = [validate_months])


class EducationQualifications(ValidateOnSaveMixin, models.Model):

    candidate = models.ForeignKey(Candidate)
    highest_qualification = models.CharField(max_length = 40, validators = [validate_highest_qualifications ])
    education_specialization = models.CharField(max_length = 40, validators = [ validate_length ])
    institute_name = models.CharField(max_length = 50, validators = [validate_length ])
