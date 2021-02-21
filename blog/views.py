from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views import View

def home(request):
    last_twenty = Post.objects.filter(
        isPublish=True).select_related('author__user_profile').order_by('-id')[:20]
    return render(request, 'index.html', {'posts': last_twenty})
    
# def PostDeleteView(View):
#     def post(self, request, id=None, *args, **kwargs):
#         context = {}
#         obj = self.get_object()
#         if obj is not None:
#             obj.delete()
#             context['object'] = None
#             return redirect('/')
#             return render(request, self.template_name, context)
        
# def logIn(request):
#     if request.method == 'POST':
#         # if post, then authenticate (user submitted username and password)
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     # return HttpResponse('<h1>Success</h1>')
#                     print(user.id)
#                     return HttpResponseRedirect('/')
#                 else:
#                     HttpResponse('<h1>Try Again</h1>')

#                     # print("The account has been disabled.")
#             else:
#                 print("The username and/or password is incorrect.")
#     else:
#         form = LoginForm()
#     return render(request, 'logIn.html', {'form': form})

# def logIn(request):
#     return render(request, 'logIn.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('HEY', user.username, 'id ', user.id)
            # HttpResponse('<h1>Success</h1>')
            # return HttpResponseRedirect('')
            return HttpResponseRedirect('/', user.id)
        else:
            print('try again')
            HttpResponse('<h1>Try Again</h1>')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def post_show(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post/show.html', {'post': post})

@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content', 'post_img', 'category_id', 'author']
    success_url = 'user/posts/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/user/posts/')

@method_decorator(login_required, name='dispatch')
class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'post_img', 'category_id', 'author']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/post/' + str(self.object.pk))

@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
  model = Post
  success_url = '/'

@login_required           
def profile(request, username):
    user = User.objects.get(username=username)
    post = Post.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'post': post})

  


def category_view(request, category_name):
    categorys_post = categorys.objects.get(category_name=category_name)
    post = Post.objects.filter(category_id=categorys_post)
    return render(request, 'category/category.html', {'category_name': category_name, 'posts': post , 'category_info':categorys_post})
 

def published(request):
    notPublished = Post.objects.filter(isPublish='notPublished')
    return render(request, 'post/publish_manage.html', {'notPublished': notPublished})
# Query to


def userPostsList(request):
    current_user = request.user
    posts = Post.objects.all().order_by('-id')
    print(posts)
    return render(request, 'userPostsList.html', {'posts': posts})


def userPublishedPostsList(request):
    current_user = request.user
    posts = Post.objects.filter(isPublish="published")
    # print(current_user.id)
    # print(current_user.username)
    print(posts)
    return render(request, 'userPostsList.html', {'posts': posts})


def userNotPublishedPostsList(request):
    current_user = request.user
    posts = Post.objects.filter(isPublish="notPublished")
    # print(current_user.username)
    print(posts)
    return render(request, 'userPostsList.html', {'posts': posts})


def userRefusedPostsList(request):
    current_user = request.user
    posts = Post.objects.filter(isPublish="refused")
    # print(current_user.id)
    # print(current_user.username)
    print(posts)
    return render(request, 'userPostsList.html', {'posts': posts})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class categoryCreate(CreateView):
    print('create new category')
    model = categorys
    fields = '__all__'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')


def profile(request):
    # current_user = request.user.id
    # posts = user_profile.objects.filter(id=current_user)
    return render(request, 'user/profile.html')
