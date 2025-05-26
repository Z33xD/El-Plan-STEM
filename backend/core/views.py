from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html',{"name":'home'})

def aboutus(request):
    return render(request,'aboutus.html',{"name":'about us'})



