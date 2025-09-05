from django.shortcuts import render

def show_main(request):
    context = {
        'appname' : 'Ball-Ballan',
        'npm' : '2406495666',
        'name': 'Rexy Adrian Fernando',
        'class': 'PBP D'
    }

    return render(request, "main.html", context)