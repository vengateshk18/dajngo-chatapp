from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
def login_page(request):
    page="login"
    if request.user.is_authenticated:
       return redirect('home')
    if request.method=='POST':
       name=request.POST.get('username')
       password=request.POST.get('password')
       #print(password)
       user=authenticate(request,username=name,password=password)
       if user is not None:
         login(request,user)
         messages.success(request,'Login success!!!')
         return redirect('home')
       else:
          messages.error(request,'invalid username or password')
          return redirect('login')
    return render(request,'login.html',{"page":page})
def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      messages.success(request,'logout success!!!')
      return redirect('home')
   else:
      messages.error(request,'user not authenticated')
      return redirect('home')
      
def home(request):
   q=request.GET.get('q')if request.GET.get('q')!=None else ''
   topic=Topic.objects.all()
   topic_count=topic.count()
   last_five_messages = Message.objects.all().order_by('-created')[:5]
   room=Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)
   ) 
   room_count=room.count()
   return render(request,'home.html',{'room':room,'topics':topic,'room_count':room_count,'recent_message':last_five_messages,'topic_count':topic_count})
@login_required(login_url='login')
def createRoom(request):
   topic=Topic.objects.all()
   form=RoomForm()
   if request.method=='POST':
      print(request.POST)
      form=RoomForm(request.POST)
      if form.is_valid:
         room=form.save(commit=False)
         room.host=request.user
         room.save()
         return redirect('home')
   context={'form':form,'topics':topic}
   return render(request,'create-room.html',context)
def updateRoom(requst,pk):
   valuue=Room.objects.get(id=pk)
   form=RoomForm(instance=valuue)
   if requst.method=='POST':
      form=RoomForm(requst.POST,instance=valuue)
      if form.is_valid:
         form.save()
         return redirect('home')
   context={'form':form}
   return render(requst,'create-room.html',context)
def deleteRoom(requset,pk):
   room=Room.objects.get(id=pk)
   if requset.method=='POST':
      room.delete()
      return redirect('home')
   return render(requset,'delete.html',{'obj':room})
def register(request):
   form=UserCreationForm()
   if request.method=='POST':
      form=UserCreationForm(request.POST)
      if form.is_valid():
         user=form.save(commit=False)
         user.username=user.username.lower()
         user.save()
         login(request,user)
         return redirect('home')
      else:
         messages.error(request,'An error occured while registration')
   return render(request,'register.html',{"form":form})
def room(request,pk):
   room=Room.objects.get(id=pk)
   participants=room.participants.all()
   if request.method=='POST':
      messagec=Message.objects.create(
         user=request.user,
         room=room,
         body=request.POST.get('commend')
      )
      room.participants.add(request.user)
      return redirect('room',pk=room.id)
   message=room.message_set.all().order_by('-created')
   return render(request,'room.html',{"room":room,"messages1":message,"participants":participants})
@login_required(login_url='login')
def delete_message(request,pk,rid):
      message=Message.objects.get(id=pk)
      print(message.user,request.user)
      if request.user==message.user:
         message.delete()
         messages.success(request,"message deleted successfully ")
         return redirect('room',pk=rid)
      else:
        messages.error(request,"you cannot delete message")
        return redirect('room',pk=rid)
def profile(request,pk):
   user=User.objects.get(id=pk)
   rooms=user.room_set.all()
   topic=Topic.objects.all()
   last_five_messages = user.message_set.all().order_by('-created')[:5]
   context={"user":user,'room':rooms,"topics":topic,'recent_message':last_five_messages}
   return render(request,'profile.html',context)