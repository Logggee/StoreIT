# login_view.py

from storage.forms import User_Login_Form
from django.contrib.auth.views import LoginView

class User_Login(LoginView):
    """ Class base standart login in view from Django

    This is used because a costum authentication form is used to apply bootstrap styling.
    Also the current logged in user needs to be set in the context.

    Inherits:
        LoginView
    """
    # Set the costum form with bootstrap sytling
    authentication_form = User_Login_Form
    # Check if a user is logged in and set it to the context
    def get_context_data(self, **kwargs) -> dict[str, object]:
        # Get the current context
        context = super().get_context_data(**kwargs)
        # Set the request.user to the context that gets renderd
        context["current_user"] = self.request.user
        return context