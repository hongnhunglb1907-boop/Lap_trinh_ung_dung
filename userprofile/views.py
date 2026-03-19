from django.shortcuts import render

def profiles(request):
    return render(request, "profile_list.html")