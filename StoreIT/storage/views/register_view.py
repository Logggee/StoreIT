# register_view.py

from django.shortcuts import get_object_or_404, render, redirect
from storage.forms import User_Registration_Form
from django.contrib.auth.views import LoginView

def register(request):
    """ /register/

    Endpoint for new user registration. The form is the UserCreationForm but all
    field are overwritten to add costum bootstrap styling to all input fields.

    Args:
        request: HTTP request object

    Returns:
        Renders the template registration.html or 
        redirects to login after a successfull registration
    """
    # Post request a user wants to register
    if request.method == "POST":
        user_registration_form = User_Registration_Form(request.POST)
        # Check if the form input where all valid
        if user_registration_form.is_valid():
            # Safe the new user in the db
            user_registration_form.save()
            return redirect("storage:login")
        
        # The registration form was not valid
        else:
            content = {"user_registration_form": user_registration_form,
                       "current_user": request.user}
            return render(request, "registration/registration.html", content)
        
    # Get request render the registration template
    else:
        content = {"user_registration_form": User_Registration_Form(),
                   "current_user": request.user}
        return render(request, "registration/registration.html", content)