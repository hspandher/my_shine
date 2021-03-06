import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mini_shine.models import Candidate

import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        try:
            Candidate.objects.all()[0].delete()
        except:
            pass
        self.browser.quit()

    def assert_element_exists_by_name(self, name, tag_name):
        elements = self.browser.find_elements_by_tag_name(tag_name)
        self.assertIn(name, [element.text for element in elements])

    def find_tag_by_display_value(self, tag_name, display_value):
        for element in self.browser.find_elements_by_tag_name(tag_name):
            if display_value in element.text:
                return element

        raise AssertionError("No element having tag {tag_name} and value {display_value}".format(tag_name = tag_name, display_value = display_value))

    def fill_input_text_field(self, field_names_to_values):
        for field_name in field_names_to_values:
            input_field = self.browser.find_element_by_name(field_name)
            input_field.send_keys(field_names_to_values[field_name])

    def check_checkboxes(self, checkbox_names_to_bool):
        for checkbox_name in checkbox_names_to_bool:
            if checkbox_names_to_bool[checkbox_name]:
                checkbox = self.browser.find_element_by_name(checkbox_name)
                if not checkbox.is_selected():
                    checkbox.click()

    def check_radio_button(self, button_name, button_value):
        self.browser.find_element_by_css_selector("input[type='radio'][value='{value}']".format(value = button_value)).click()


    def fill_and_submit_form(self, details):
        input_fields_details = {}
        checkbox_details = {}
        for field_name in details:
            if type(details[field_name]) == str:
                if field_name == 'radio':
                    self.check_radio_button(field_name, details[field_name])
                else:
                    input_fields_details[field_name] = details[field_name]
            if type(details[field_name]) == bool:
                checkbox_details[field_name] = details[field_name]

        self.fill_input_text_field(input_fields_details)
        self.check_checkboxes(checkbox_details)

        self.browser.find_element_by_css_selector('input[type="submit"]').click()

    def test_home_page_has_right_title_and_register_button(self):
        # Edith has heard about cool new mini-job portal. She goes to its homepage to
        # check it out

        self.browser.get('http://localhost:8000')

        # She notices that the page has title Mini Shine and a header with the same word
        self.assertIn('Mini Shine', self.browser.title)
        self.assertIn('Welcome to Mini Shine!', [element.text for element in self.browser.find_elements_by_tag_name('h1')])

        # She notices the 'Register Now!' button in the top right corner.
        self.assert_element_exists_by_name('Register Now!', 'a')

    def test_can_register_and_redirect_to_profile(self):
        # She goes to the home page
        self.browser.get('http://localhost:8000')

        # She clicks it, which redirects her to another page with a form.
        self.find_tag_by_display_value('a', 'Register Now!').click()
        self.assertIn('/register/', self.browser.current_url)

        # The form requires her to fill Email, Password, Confirm Password, Mobile Number, city, country and gender
        self.browser.find_element_by_css_selector("input[placeholder='Email']")
        self.browser.find_element_by_css_selector("input[placeholder='Password']")
        self.browser.find_element_by_css_selector("input[placeholder='Confirm Password']")
        self.browser.find_element_by_css_selector("input[placeholder='Mobile Number']")
        self.browser.find_element_by_css_selector('input[type="radio"][name="gender"]')
        self.browser.find_element_by_css_selector("input[placeholder='First Name']")
        self.browser.find_element_by_css_selector("input[placeholder='Last Name']")


        # and checkbox for terms and conditions

        # She fills the form with:-
        # email:- 'edith432@gmail.com'

        # password:- 'edith3099'

        # confirm_password:- 'edith3099'

        # first_name:- 'Edith'

        # last_name:- 'Nash'

        # city:- 'Massachussets'

        # country:- 'USA'

        # mobile_no:- '9934734234'

        # She agrees to terms and conditions

        # She clicks the button 'Register'

        details = {'email': 'edith432@gmail.com', 'first_name': 'Edith', 'last_name': 'Nash', 'city': 'Massachussets', 'country': 'USA' , 'password': 'edith3099', 'confirm_password': 'edith3099', 'mobile_number': '9934734234', 'terms_and_conditions': True, 'radio': 'M'}

        self.fill_and_submit_form(details)

        time.sleep(5)


        # She is redirected to a rather long form asking of lot of details.
        self.assertRegexpMatches(self.browser.current_url ,r'candidate\/\d{1,10}\/add-work-experience\/$')


        # Work Experience :-
        # Are you:- Fresher, Experienced
        # Total Experience:- Select Years, Select Months

        # She considers her as having professional experience

        self.browser.find_element_by_css_selector('input[type="checkbox"][name="is_experienced"]').click()

        # She selects 10 years as years of experience

        self.browser.find_element_by_xpath("//select[@name='years_of_experience']/option[@value='10']").click()

        # She selects 3 months as months of experience

        self.browser.find_element_by_xpath("//select[@name='months_of_experience']/option[@value='3']").click()

        # She click the next button

        self.browser.find_element_by_css_selector("input[type='submit'][value='Next']").click()

        # Educational Details :-
        # Highest Qualification:- Post-Graduate, Graduate, XII, X
        # She selects XII, she is asked to fill board/Institution, College/University,
        # and Marks/CGP of each of them.

        # Finally, She clicks the submit button

        time.sleep(5)

        self.browser.find_element_by_xpath("//select[@name='highest_qualification']/option[@value='10+2']").click()

        self.browser.find_element_by_css_selector("input[type='text'][name='education_specialization']").send_keys('Non-Medical')

        self.browser.find_element_by_name('institute_name').send_keys('CBSE')

        self.browser.find_element_by_css_selector("input[type='submit'][value='Submit']").click()

        # She is redirected to her profile, with all her details and
        # credentials

        self.assertRegexpMatches(self.browser.current_url ,r'candidate\/\d{1,10}\/profile\/$')

        time.sleep(10)

        # Profile page has all her credentials

        # She is satisfied and quit the browser

        self.login_to_profile()

    def login_to_profile(self):
        # she visits the login page
        self.browser.get('http://localhost:8000/login')

        # she fills the email field as 'edith432@gmail.com'
        self.browser.find_element_by_css_selector("#base-form input[name='email']").send_keys('edith432@gmail.com')

        # She fills the password field
        self.browser.find_element_by_css_selector("#base-form input[name='password']").send_keys('edith3099')

        # She presses the login button
        self.browser.find_element_by_css_selector("#base-form input[type='submit'][value='Login']").click()

        time.sleep(20)

        # She is redirected to her profile page
        self.assertRegexpMatches(self.browser.current_url ,r'candidate\/\d{1,10}\/profile\/$')



if __name__ == '__main__':
    unittest.main()
