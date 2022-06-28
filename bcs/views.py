from django.shortcuts import render

def HomeScreen(request):
    return render(request, "index.html")