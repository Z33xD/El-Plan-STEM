from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chatbot import get_chat_response

# Create your views here.
def chat(request):
    return render(request,'chatbot.html',{"name":'chatbot'})

@csrf_exempt
def chat_endpoint(request):
    if request.method == 'POST':
        try:
            data = request.POST
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            response = get_chat_response(user_message)
            return JsonResponse({'response': response})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)