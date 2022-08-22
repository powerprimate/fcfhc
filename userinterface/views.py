from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login


# Create your views here.
def studentlogin(request):
    if 'a_username' in request.session:
        return redirect('database')
    if 'username' in request.session:
        return redirect('home')
    if 'logout' in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        student = authenticate(username=username,password=password)
        if User.is_superuser:
            messages.info(request,'Invalid login..!')
            return redirect('login')
        else:
            if student is not None:
                login(request ,student)
                request.session['username'] = username
                return redirect('home')
            else:
                messages.info(request,'Invalid credentials..!')
                return redirect('login')
    else:
        return render(request,'studentlogin.html')
    
def studentlogout(request):
    if 'username' in request.session:
        request.session.flush
    request.session['logout'] = logout
    logout(request)
    return redirect('login')

def studentregister(request):
    if 'username' in request.session:
        return redirect('home')
    elif 'a_username' in request.session:
        return redirect('database')
    
    if  request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists() or User.objects.filter(password=password).exists():       
            if  User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists.!!!')
                 
            if User.objects.filter(username=username).exists():
                messages.info(request,'username is taken.!!!')
           
            return redirect('register')
            
        else:
            student = User.objects.create_user(first_name=first_name, last_name=last_name, email=email , password=password, username=username,)
            student.save()
            return redirect('login')
            
    else:   
        return render(request,'studentsignup.html')

def home(request):
    if 'a_username' in request.session:
        return redirect('database')
    if 'username' in request.session:
        return render(request,'home.html')
    
    return redirect('login')
    
    
