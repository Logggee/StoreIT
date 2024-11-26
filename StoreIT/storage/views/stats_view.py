# stats_view.py

from django.shortcuts import render

def stats(request):
    ''' /stats
    Stats page

    Args:
        request: HTTP request object

    Returns:
        Renders the template stats.html
    '''
    return render(request, "storage/stats.html")