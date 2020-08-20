from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import task
from django.contrib import messages
import smtplib
import time
import datetime as dt
import threading
import urllib.request
import urllib.parse
 

timelist = {}
# Create your views here.

def todohome(request):
    threadObj = threading.Thread(target=emails)
    threadObj.start()
    if request.user.is_authenticated:
        tasks = task.objects.filter(owner=request.user.pk)
        return render(request,'todohome.html',{'tasks':tasks})
    else:
        return render(request,'todohome.html')

def add(request):
    if request.user.is_authenticated:
        blog1 = task()
        now = dt.datetime.now() 
        blog1.date = request.POST['date']
        blog1.time = request.POST['time']
        time = now.strftime("%H:%M")
        tday = now.strftime("%Y-%m-%d")
        if time > blog1.time:
            messages.info(request,"We are working on time travel...")
            return redirect('todohome')
        if tday > blog1.date:
            messages.info(request,"A date before today can't be reminded...")
            return redirect('todohome')
        blog1.content = request.POST['content']
        blog1.owner = request.user.pk
        blog1.save()
        timelist[int(request.user.pk)*1000+int(blog1.pk)]= blog1.date +" "+ blog1.time + ":00"
        return redirect('todohome')
    else:
        return redirect('login')

def delete(request,pk):
    a = get_object_or_404(task,pk=pk)
    a.delete()
    return redirect('todohome')

def sendSMS(apikey, numbers, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 


def send_email(send_to,ta):
    email_user = 'shuvanshugupta101@gmail.com'
    server = smtplib.SMTP ('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, 'wuapigkkusfnzqym')

    #EMAIL
    message = 'Have you forgot this task\nTask: '+ str(ta.content)+'\nToDo- A Reminder Web Application'
    server.sendmail(email_user, send_to , message)
    server.quit()

def send_email_at(send_time,send_to,ta,u):
    time.sleep(send_time.timestamp() - time.time())
    send_email(send_to,ta)
    print('email sent')
    resp =  sendSMS('c49igJPDn1Q-URH8PBcuvPcpP6Pk2Cj5ixxkpSvPf8', '91'+str(u.last_name),'Have you forgot this task\nTask: '+ str(ta.content)+'\nToDo- A Reminder Web Application')
    print (resp)
    print('message sent')
    ta.delete()

def emails():
    for it in sorted(timelist):
        send_time = dt.datetime.strptime(timelist[it],"%Y-%m-%d %H:%M:%S")
        u = get_object_or_404(User,pk=int(it)//1000)
        ta = get_object_or_404(task,pk=int(it)%1000)
        send_to = u.email
        print(u.email)
        print(u.first_name)
        print(u.last_name)
        timelist.pop(it)
        send_email_at(send_time,send_to,ta,u)



