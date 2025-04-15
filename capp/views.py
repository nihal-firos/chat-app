from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def index(request):
    return render(request, 'index.html')

def room(request, room):
    username = request.GET.get('username')
    try:
        room_details = Room.objects.get(name=room)
        return render(request, 'room.html', {
            'username': username,
            'room': room,
            'room_details': room_details,
        })
    except Room.DoesNotExist:
        # Redirect to home page if room doesn't exist
        return redirect('/')  # Or show an error message

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_name = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_name)
    new_message.save()
    return JsonResponse('success')

def getMessages(request, room):
    try:
        room_details = Room.objects.get(name=room)
        messages = Message.objects.filter(room=room_details.id)
        return JsonResponse({"messages": list(messages.values())})
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)