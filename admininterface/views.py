


from .forms import CRUDFORM
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
def admincreateuser(request):
    if 'username' in request.session:
        return redirect('home')
    
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
                
            if User.objects.filter(password=password).exists():
                messages.info(request,'password is taken.!!!')
           
            return redirect('create')
            
        else:
            student = User.objects.create_user(first_name=first_name, last_name=last_name, email=email , password=password, username=username,)
            student.save()
            return redirect('database')
            
    else:   
        return render(request,'admincreateuser.html')


def adminlogin(request):
    
    if 'username' in request.session:
        return redirect('home')
    elif 'a_username' in request.session:
        return redirect('database')
    elif 'logout' in request.session:
        return redirect('adminlogin')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        teacher = authenticate(username=username,password=password)
        if teacher is not None:
            if teacher.is_superuser:
                request.session['a_username']=username
                login(request,teacher)
                return redirect ('database')
        else:
            messages.info(request,'Invalid credentials..!')
            return redirect('adminlogin')
    else:
        return render(request,'adminlogin.html')
    
def adminlogout(request):
    if 'a_username' in request.session:
        request.session.flush
    request.session['logout'] = logout
    logout(request)
    return redirect('adminlogin')

def admindatabase(request):
    if 'username' in request.session:
        return redirect('home')
    if 'a_username' in request.session:
        if 'q' in request.GET:
            q = request.GET['q']
            user = User.objects.filter(Q(username__icontains=q)|Q(first_name__icontains=q))
        else:
            user = User.objects.all()
        context = {'users':user}        
        return render(request,'studentdatabase.html',context)
    else:
        return redirect('adminlogin')

def adminupdation(request, id=None):  
    if 'username' in request.session:
        return redirect('home')
    try:
        user = User.objects.get(id=id)
        form=CRUDFORM (instance=user)
        if request.method == 'POST':
            form=CRUDFORM(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('database')
        context = {'form':form}
        return render (request,"adminupdateuser.html",context)
    except:
        messages.info(request,"user doesn't exist")
        return redirect('database')

def admindelete(request,id=None):
    if 'username' in request.session:
        return redirect('home')
    User.objects.filter(id=id).delete()
    return redirect('database')

