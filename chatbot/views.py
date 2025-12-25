from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage

def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        # Simple bot response (can be enhanced with AI)
        bot_response = f"You said: {user_message}. How can I help you with travel?"
        
        # Save to database
        ChatMessage.objects.create(
            user_message=user_message,
            bot_response=bot_response
        )
        
        return JsonResponse({'response': bot_response})
    
    return render(request, 'chatbot.html')
