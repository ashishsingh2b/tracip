from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpFrom,LoginFrom,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    posts =Post.objects.all()
    return render(request,'home.html',{'posts':posts})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginFrom(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Log in successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginFrom()  
        return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return HttpResponseRedirect('/')

def user_signup(request):
 if request.method=="POST":
    form=SignUpFrom(request.POST)
    if form.is_valid():
      messages.success(request,"Congratulations!! You have become an Author")
      user = form.save()
      group = Group.objects.get(name='Author')
      user.groups.add(group)
 else:     
  form =SignUpFrom()
 return render(request,'signup.html',{'form':form})

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        ip = request.session.get('ip',0)
        return render(request, 'dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': groups,'ip':ip})
    else:
        return HttpResponseRedirect('/login/')
  
def add_post(request):
   if request.user.is_authenticated:
    if request.method == "POST":
       form = PostForm(request.POST)
       if form.is_valid():
          title =form.cleaned_data['title']
          desc = form.cleaned_data['desc']
          pst = Post(title=title,desc= desc)
          pst.save()
          form = PostForm()
    else:
      form= PostForm()
    return render(request,'addpost.html',{'form':form})
   else:
      return HttpResponseRedirect('/login/')
   
def edit(request,id):
   if request.user.is_authenticated:
     if request.method == "POST":
        pi = Post.objects.get(pk=id)
        form=PostForm(request.POST,instance=pi)
        if form.is_valid():
         form.save()
        return HttpResponseRedirect('/dashboard/')
     else:
        pi=Post.objects.get(pk=id)
        form = PostForm(instance=pi)
     return render(request,'updatepost.html',{'form':form})
   else:
     return HttpResponseRedirect('/login/')
   
def delete(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
           pi = Post.objects.get(pk=id)
           pi.delete()
           return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


