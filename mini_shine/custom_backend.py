from mini_shine.models import Candidate

class CandidateBackend:

    def authenticate(self, email = None, password = None):

        try:
            user = Candidate.objects.get(email = email)

            if password == user.password:
                return user
            else:
                return None
        except:
            return None


    def get_user(self, user_id):
        try:
            return Candidate.objects.get(id = user_id)
        except:
            return None
