from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user =User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return User.objects.filter(email =username).order_by('id').first()
        
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            
        except User.DoesNotExist:
            return None
        
        return user if self.user_can_authenticate(user) else None