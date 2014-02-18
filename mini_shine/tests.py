from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from rest_framework.test import APIRequestFactory
from mini_shine.views import home, register, add_work_experience
from mini_shine.forms import RegistrationForm, WorkExperienceForm
from mini_shine.models import Candidate, WorkExperience, EducationQualifications


import pdb

class PageTestMethodsMixin:

    def submit_post_form_to_view(self, link, form_details):
        factory = APIRequestFactory()
        request = factory.post(link, form_details)
        return register(request), RegistrationForm(request.POST)

class ModelTestMethodsMixin:

    def is_valid(self, object_name):
        try:
            getattr(self, object_name).save()
        except:
            return False
        else:
            return True

    def verify_all_validations(self, object_name, attribute_name, invalid_attributes):
        for invalid_attribute in invalid_attributes:
            target_object = getattr(self, object_name)
            setattr(target_object, attribute_name, invalid_attribute)
            if self.is_valid(object_name):
                self.fail("{attr_value} should not be a valid {attribute_name}, but it passes".format(attr_value = invalid_attribute, attribute_name = attribute_name))


class HomePageTest(TestCase):

    def setUp(self):
        self.response = home(HttpRequest())

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_return_html_response(self):
        self.assertIsInstance(self.response, HttpResponse)

    def test_home_view_renders_a_template(self):
        expected_response = render_to_response('home.html')
        self.assertEqual(self.response.content, expected_response.content)

    def test_home_page_has_right_title(self):
        self.assertIn('<title>Mini Shine</title>', self.response.content)

    def test_home_page_has_right_header(self):
        self.assertIn('<h1>Welcome to Mini Shine!</h1>', self.response.content)

    def test_home_page_has_register_now_link(self):
        self.assertRegexpMatches(str(self.response.content), r'<a(.|\n)*Register Now!(.|\n)*<\/a>')

    def test_register_now_link_has_right_url(self):
        self.assertRegexpMatches(self.response.content, r'<a(.|\n)*?\/register\/(.|\n)*?>(.|\n)*?Register Now!(.|\n)*?<\/a>', 'Register Now link doesn\'t have right url')


class RegisterPageTest(PageTestMethodsMixin, TestCase):

    def setUp(self):
        self.response = register(HttpRequest())
        self.form_details = {
                'email': 'hspandher2@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit3242',
                'mobile_number': '9347384284',
                'terms_and_conditions': 'checked',
                'first_name': 'Hakampreet Singh',
                'last_name': 'Pandher',
                'country': 'India',
                'city': 'Ludhiana',
                'gender': 'M'
            }

    def check_registration_validation(self, form_details):
        link = '/register/'
        response, form = self.submit_post_form_to_view(link, form_details)
        expected_response = render_to_response('register.html', {'form': form})
        self.assertEqual(expected_response.content, response.content)

    def test_register_url_points_to_view(self):
        found = resolve('/register/')
        self.assertEqual(found.func, register)

    def test_register_view_return_http_response(self):
        self.assertIsInstance(self.response, HttpResponse)

    def test_register_view_uses_right_template(self):
        form = RegistrationForm()
        expected_response = render_to_response('register.html', { 'form': form })
        self.assertEqual(expected_response.content, self.response.content)

    def test_register_view_has_right_title_and_header(self):
        self.assertIn('<title>Register</title>', self.response.content)
        self.assertIn('<h1>Register</h1>', self.response.content)

    def test_register_view_has_form_tag(self):
        self.assertIn('form', self.response.content)

    def test_register_view_has_correct_form_fields(self):
        input_fields_names = ['email', 'password', 'confirm_password', 'mobile_number', 'gender', 'first_name', 'last_name', 'city', 'country']
        for field_name in input_fields_names:
            self.assertIn(field_name, self.response.content)

    def test_register_view_redirects_after_registration(self):
        link = '/register/'
        response, placeholder = self.submit_post_form_to_view(link, self.form_details)
        self.assertEqual(response.status_code, 302)

    def test_register_view_does_not_redirect_after_error_form_info(self):
        self.form_details['mobile_number'] = '9347384284324234243343'
        self.check_registration_validation(self.form_details)

    def test_register_view_does_not_accept_invalid_email(self):
        self.form_details['email'] = 'hspandhe.r@outlook@com'
        self.check_registration_validation(self.form_details)

    def test_register_view_does_not_accept_mobile_number(self):
        self.form_details['mobile_number'] = '934738428432323232'
        self.check_registration_validation(self.form_details)

    def test_register_view_does_not_accept_if_terms_not_agreed(self):
        self.form_details['terms_and_conditions'] = False
        self.check_registration_validation(self.form_details)

    def test_register_view_not_accept_if_password_not_match_confirm_password(self):
        self.form_details['confirm_password'] = 'foo'
        self.check_registration_validation(self.form_details)


    def test_register_view_does_not_accept_if_fields_are_missing(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'mobile_number': '9347384284',
                'terms_and_conditions': False
            }
        self.check_registration_validation(form_details)

    def test_candidate_model_creates_when_register_form_details_are_ok(self):
        self.submit_post_form_to_view('/register/', self.form_details)
        self.assertTrue(Candidate.objects.filter(email = self.form_details['email']))


class CandidateModelTest(ModelTestMethodsMixin, TestCase):

    def setUp(self):
        self.candidate = Candidate(
            email = 'hspandher@outlook.com',
            first_name = 'Hakampreet Singh',
            last_name = 'Pandher',
            country = 'India',
            city = 'Ludhiana',
            gender = 'M',
            password = 'punit1988',
            mobile_number = '9738472222')

    def is_candidate_valid(self):
        return self.is_valid('candidate')

    def has_appropriate_validation(self, attribute_name, invalid_attributes = ['', 'aa', 'j'*51]):
        self.verify_all_validations('candidate', attribute_name, invalid_attributes)

    def test_candidate_rejects_invalid_email(self):
        invalid_emails = ['lsflsdjf', 'ksjfls@slfls', 'lsjfldsfj.com']
        self.has_appropriate_validation('email', invalid_emails)

    def test_candidate_rejects_invalid_first_name(self):
        self.has_appropriate_validation('first_name')

    def test_candidate_rejects_invalid_last_name(self):
        self.has_appropriate_validation('last_name')

    def test_candidate_rejects_invalid_city(self):
        self.has_appropriate_validation('city')

    def test_candidate_rejects_invalid_country(self):
        self.has_appropriate_validation('country')

    def test_candidate_rejects_invalid_gender(self):
        invalid_genders = ['a', 'sjf', '1', 'slfsl']
        self.has_appropriate_validation('gender', invalid_genders)

    def test_candidate_rejects_invalid_mobile_number(self):
        invalid_mobile_numbers = ['342424', '3242', '134242432a', 'slfsl']
        self.has_appropriate_validation('gender', invalid_mobile_numbers)

    def test_valid_candidate_is_accepted(self):
        self.assertTrue(self.is_candidate_valid())

    def test_candidate_with_already_existing_email_is_rejected(self):
        self.candidate.save()
        self.assertFalse(self.is_candidate_valid())


class WorkExperienceModelTest(ModelTestMethodsMixin, TestCase):

    def setUp(self):
        self.candidate = Candidate(
            email = 'hspandher@outlook.com',
            first_name = 'Hakampreet Singh',
            last_name = 'Pandher',
            country = 'India',
            city = 'Ludhiana',
            gender = 'M',
            password = 'punit1988',
            mobile_number = '9738472222')

        self.candidate.save()

        self.work_experience = WorkExperience(
            candidate = self.candidate,
            is_experienced = True,
            years_of_experience = 3,
            months_of_experience = 10)

    def is_work_experience_valid(self):
        return self.is_valid('work_experience')

    def has_appropriate_validation(self, attribute_name, invalid_attributes):
        self.verify_all_validations('work_experience', attribute_name, invalid_attributes)

    def test_work_experience_belongs_to_valid_candidate(self):
        Candidate.objects.get(email = self.work_experience.candidate.email).delete()
        self.assertFalse(self.is_work_experience_valid(), 'Work Experience Candidate does not exist in the database')

    def test_work_experience_rejects_invalid_years_of_experience(self):
        invalid_years = [342, -10, -4, 100, 1700, -1, 99]
        self.has_appropriate_validation('years_of_experience', invalid_years)

    def test_work_experience_rejects_invalid_months_of_experience(self):
        invalid_months = [-2, 13, -1, 234]
        self.has_appropriate_validation('months_of_experience', invalid_months)

    def test_work_experience_rejects_invalid_is_experienced_value(self):
        invalid_is_experienced_values = [32, '2', 'yes', 4]
        self.has_appropriate_validation('is_experienced', invalid_is_experienced_values)


class WorkExperiencePageTest(PageTestMethodsMixin, TestCase):

    def setUp(self):
        self.candidate = Candidate(
            email = 'hspandher@outlook.com',
            first_name = 'Hakampreet Singh',
            last_name = 'Pandher',
            country = 'India',
            city = 'Ludhiana',
            gender = 'M',
            password = 'punit1988',
            mobile_number = '9738472222')

        self.candidate.save()
        self.url = "/candidate/{id}/add-work-experience/".format(id = self.candidate.id)
        self.response = add_work_experience(HttpRequest(), self.candidate.id)
        self.form_details = {
            'is_experienced': True,
            'years_of_experience': 4,
            'months_of_experience': 5
        }

    def test_work_url_resolves_to_right_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, add_work_experience)

    def test_work_view_returns_http_response_object(self):
        self.assertIsInstance(self.response, HttpResponse)

    def test_work_view_uses_right_template(self):
        expected_response = render_to_response('work_experience.html', { 'form': WorkExperienceForm()})
        self.assertEqual(expected_response.content, self.response.content)

    def test_work_view_has_right_title(self):
        self.assertIn('<title>Add Work Experience</title>', self.response.content)

    def test_work_view_has_right_header(self):
        self.assertIn('<h1>Add Work Experience</h1>', self.response.content)

    def test_work_view_has_correct_form_fields(self):
        input_fields_names = ['years_of_experience', 'months_of_experience', 'is_experienced']
        for field_name in input_fields_names:
            self.assertIn(field_name, self.response.content)

    def test_work_view_redirects_after_successful_submission(self):
        response, _ = self.submit_post_form_to_view(self.url, self.form_details)
        self.assertEqual(response.status_code, 302)


class EducationQualificationsModelTest(ModelTestMethodsMixin, TestCase):

    def setUp(self):
        self.candidate = Candidate(
            email = 'hspandher@outlook.com',
            first_name = 'Hakampreet Singh',
            last_name = 'Pandher',
            country = 'India',
            city = 'Ludhiana',
            gender = 'M',
            password = 'punit1988',
            mobile_number = '9738472222')

        self.candidate.save()

        self.work_experience = WorkExperience(
            candidate = self.candidate,
            is_experienced = True,
            years_of_experience = 3,
            months_of_experience = 10)

        self.work_experience.save()

        self.education_qualifications = EducationQualifications(
            candidate = self.candidate,
            highest_qualification = '10+2',
            education_specialization = 'Non-Medical',
            institute_name = 'CBSE')

    def are_qualifications_valid(self):
        return self.is_valid('qualifications')

    def has_appropriate_validation(self, attribute_name, invalid_attributes):
        self.verify_all_validations('education_qualifications', attribute_name, invalid_attributes)

    def test_qualifications_belong_to_valid_candidate(self):
        Candidate.objects.get(email = self.candidate.email).delete()
        self.assertFalse(self.are_qualifications_valid(), 'Candidate with created qualifications does not exists in the database')

    def test_qualifications_rejects_invalid_highest_qualification(self):
        invalid_highest_qualifications = ['ldfjdslf', 'sdjfdls', '10+2ldsjfl']
        self.has_appropriate_validation('highest_qualification', invalid_highest_qualifications)