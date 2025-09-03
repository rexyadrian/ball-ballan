from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406495666',
        'name': 'Rexy Adrian Fernando',
        'class': 'PBP D'
    }

    return render(request, "main.html", context)