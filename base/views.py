from django.db.models import Q
from django.shortcuts import render,redirect
from .models import Blog, Profile, Project, DevLog
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page': 'login'}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            password=password
        )
        login(request,user)

        return redirect('home')

    context = {'page': 'register'}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):

    query = request.GET.get('q', '').strip()
    topic = request.GET.get('topic', '').strip()

    blogs = Blog.objects.all()
    projects = Project.objects.all()

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        )

    if topic:
        blogs = blogs.filter(category__iexact=topic)

    context = {
        'blogs': blogs,
        'projects': projects,
        'query': query,
        'topic': topic,
    }

    return render(request, "base/home.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    return render(request, "base/blog.html", {'blog': blog})

@login_required
def createBlog(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        blog = Blog.objects.create(
            user=request.user,
            title=title,
            content=content,
            category=category,
        )

        return redirect('blog', pk=blog.id)

    return render(request, "base/create_blog.html")


@login_required
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)

    if(request.method == 'POST'):
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category = request.POST.get('category')

        blog.save()

        return redirect('blog', pk=blog.id)

    return render(request, "base/update.html",{'blog':blog})


@login_required
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()

        return redirect('home')

    return render(request, "base/delete.html",{'blog':blog})

def userProfile(request, pk):
    user = User.objects.get(id=pk)

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'base/profile.html', context)

@login_required
def editProfile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        profile.bio = request.POST.get('bio')

        user.save()
        profile.save()

        return redirect('profile', pk=user.id)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'base/edit_profile.html', context)


@login_required
def createProject(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')
        tech_stack = request.POST.get('tech_stack')
        github_link = request.POST.get('github_link')

        Project.objects.create(
            user=request.user,
            name=name,
            description=description,
            tech_stack=tech_stack,
            github_link=github_link
        )

        return redirect('home')

    return render(request, 'base/create_project.html')

def projectDetail(request, pk):

    project = Project.objects.get(id=pk)

    devlogs = project.devlogs.all().order_by('-created')

    milestones = project.devlogs.filter(
        log_type='milestone'
    ).order_by('-created')

    context = {
        'project': project,
        'devlogs': devlogs,
        'milestones': milestones,
    }

    return render(request, 'base/project_detail.html', context)

@login_required
def createDevLog(request, project_id):

    project = Project.objects.get(id=project_id)

    if request.method == 'POST':

        title = request.POST.get('title')
        log_type = request.POST.get('log_type')
        content = request.POST.get('content')

        DevLog.objects.create(
            project=project,
            title=title,
            log_type=log_type,
            content=content
        )

        return redirect('project-detail', pk=project.id)

    return render(
        request,
        'base/create_devlog.html',
        {'project': project}
    )







    
