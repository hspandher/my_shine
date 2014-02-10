import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_register_on_the_portal(self):
        # Edith has heard about cool new mini-job portal. She goes to its homepage to
        # check it out

        self.browser.get('http://localhost:8000')

        # She notices that the page has title Shine and a header with the same word
        self.assertIn('Shine', self.browser.title)

        # She notices the 'Register Now!' button in the top right corner.

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
        # Pending User story



if __name__ == '__main__':
    unittest.main()
