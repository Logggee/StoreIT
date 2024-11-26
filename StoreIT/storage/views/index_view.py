# index_view.py

from django.shortcuts import render

def index(request):
    """ /
    Landingpage

    Args:
        request: HTTP request object

    Returns:
        Renders the template index.html
    """
    print(f"Current User: {request.user.username}")
    content = {"current_user": request.user}
    return render(request, "storage/index.html", content)