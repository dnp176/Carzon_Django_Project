from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from loguru import logger
# Create your views here.
logger.add("log/login_log.log",level="TRACE",rotation="100 MB")
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in.')
            logger.success("login Success-" + username)
            return redirect('dashboard')
        else:
            logger.error("login Fail-" + username)
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'inquiry':user_inquiry,
    }
    return render(request,'accounts/dashboard.html',data)

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['confirm_password']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                    auth.login(request,user)
                    messages.success(request,'You are now logged in')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request,'You are successfully registered')
                    logger.success("Registered Success-" + username + '-' + email)
                    return redirect('login')

        else:
            messages.error(request,'Password do not match')
            return redirect(request,'register')

    else:
        return render(request,'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are successfully logged out.')
        return redirect('home')
    return redirect('home')
