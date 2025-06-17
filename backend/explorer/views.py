from django.shortcuts import render

# Create your views here.
def dataexp(request):
    return render(request,'explorer.html',{"name":'explorer'})