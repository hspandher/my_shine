import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assert_element_exists_by_name(self, name, tag_name):
        elements = self.browser.find_elements_by_tag_name(tag_name)
        self.assertIn(name, [element.text for element in elements])

    def find_tag_by_display_value(self, tag_name, display_value):
        for element in self.browser.find_elements_by_tag_name(tag_name):
            if display_value in element.text:
                return element

        raise AssertionError("No element having tag {tag_name} and value {display_value}".format(tag_name = tag_name, display_value = display_value))

    def fill_and_submit_registration_form(self, details):
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys(details['email'])

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(details['password'])

        confirm_password_field = self.browser.find_element_by_name('confirm_password')
        confirm_password_field.send_keys(details['confirm_password'])

        mobile_number_field = self.browser.find_element_by_name('mobile_number')
        mobile_number_field.send_keys(details['mobile_number'])

        self.browser.find_element_by_css_selector('input[type="submit"]').click()


    def test_home_page_has_right_title_and_register_button(self):
        # Edith has heard about cool new mini-job portal. She goes to its homepage to
        # check it out

        self.browser.get('http://localhost:8000')

        # She notices that the page has title Mini Shine and a header with the same word
        self.assertIn('Mini Shine', self.browser.title)
        self.assertIn('Mini Shine', [element.text for element in self.browser.find_elements_by_tag_name('h1')])

        # She notices the 'Register Now!' button in the top right corner.
        self.assert_element_exists_by_name('Register Now!', 'a')

    def test_can_register_and_redirect_to_profile(self):
        # She goes to the home page
        self.browser.get('http://localhost:8000')

        # She clicks it, which redirects her to another page with a form.
        self.find_tag_by_display_value('a', 'Register Now!').click()
        self.assertIn('/register/', self.browser.current_url)

        # The form requires her to fill Email, Password, Confirm Password, Mobile Number
        self.browser.find_element_by_css_selector("input[placeholder='Email']")
        self.browser.find_element_by_css_selector("input[placeholder='Password']")
        self.browser.find_element_by_css_selector("input[placeholder='Confirm Password']")
        self.browser.find_element_by_css_selector("input[placeholder='Mobile Number']")

        # and checkbox for terms and conditions
        self.browser.find_element_by_css_selector('input[type="checkbox"][name="terms_and_conditions"]')

        # She fills the form with:-
        # email:- 'edith432@gmail.com'

        # password:- 'edith3099'

        # confirm_password:- 'edith3099'

        # mobile_no:- '9934734234'

        # She agrees to terms and conditions

        # She clicks the button 'Register'

        details = {'email': 'edith432@gmail.com', 'password': 'edith3099', 'confirm_password': 'edith3099', 'mobile_number': '9934734234'}
        self.fill_and_submit_registration_form(details)

        # She is redirected to a rather long form asking of lot of details.

        # Personal Details :-
        # Name - first_name, last_name

        # Current Location: - select city, country
        # Gender:- Male, Female

        # Work Experience :-
        # Are you:- Fresher, Experienced
        # Total Experience:- Select Years, Select Months

        # Educational Details :-
        # Highest Qualification:- Post-Graduate, Graduate, XII, X
        # She selects XII, she is asked to fill board/Institution, College/University,
        # and Marks/CGP of each of them.

        # Resume
        # Upload resume :- Choose File

        # Finally, In the end there is a submit button
        # She is redirected to her profile, with all her details and
        # credentials

        # She is satisfied and quit the browser



if __name__ == '__main__':
    unittest.main()
