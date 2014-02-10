import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def assert_element_exists_by_name(self, name, tag_name):
        elements = self.browser.find_elements_by_tag_name(tag_name)
        self.assertIn(name, [element.text for element in elements])

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
        pass
        # She clicks it, which redirects her to another page with a form.

        # The form requires her to fill Email, Password, Confirm Password, Mobile No.
        # and checkbox for terms and conditions

        # She fills the form with:-
        # email:- 'edith43_2@gmail.com'
        # password:- 'edith3099'
        # confirm_password:- 'edith3099'
        # mobile_no:- '9934734234'

        # She clicks the button 'Sign up'

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
