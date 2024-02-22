from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.conf import settings
from random import shuffle
import json
import numpy as np
from numpy.linalg import norm
from .forms import SignupForm, LoginForm, ProjectForm, EditProject
from .models import User, Activity, ActivityGroup, Project, Student, Teacher
from django.views.decorators.http import require_POST
from django.core import serializers


def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        form = EditProject(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("user"))
    else:
        form = EditProject(instance=project)

    return render(request, 'skillmatch/edit_project.html', {"form": form, "project": project})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            cur_user = Teacher.objects.get(pk=request.user.id)
            cur_user.created_projects.add(project)
            return HttpResponseRedirect(reverse("user"))
    else:
        form = ProjectForm()
    return render(request, 'skillmatch/create.html', {'form': form})



def user_view(request):
    user = request.user
    if request.user.is_authenticated:
        if request.user.user_type == "student":
            user = Student.objects.get(pk=request.user.id)
            data = {k: v for k, v in user.__dict__.items() if k in ["id", "username", "done_test", "mechanic", "scientific", "persuasive", "artistic", "calculus", "user_type"]}
            data["saved_projects"] = list(user.saved_projects.values_list("id", flat=True))
            data["liked_projects"] = list(user.liked_projects.values_list("id", flat=True))
            data["onprogress_projects"] = list(user.onprogress_projects.values_list("id", flat=True))
            data["previous_projects"] = list(user.previous_projects.values_list("id", flat=True))
        elif request.user.user_type == "teacher":
            user = Teacher.objects.get(pk=request.user.id)
            data = {k: v for k, v in user.__dict__.items() if k in ["id", "username", "done_test", "mechanic", "scientific", "persuasive", "artistic", "calculus", "user_type"]}
            data["saved_projects"] = list(user.saved_projects.values_list("id", flat=True))
            data["liked_projects"] = list(user.liked_projects.values_list("id", flat=True))
            data["created_projects"] = list(user.created_projects.values_list("id", flat=True))
        elif request.user.is_staff:
            user = User.objects.get(pk=request.user.id)
            data = {k: v for k, v in user.__dict__.items() if k in ["id", "username", "done_test", "mechanic", "scientific", "persuasive", "artistic", "calculus", "user_type"]}
            data["saved_projects"] = list(user.saved_projects.values_list("id", flat=True))
        else:
            return JsonResponse({"error": "Invalid user type"}, status=400)
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)


def project_view(request, id):
    project = Project.objects.get(pk=id)
    liked = project in request.user.liked_projects.all()
    added = project in request.user.saved_projects.all()
    return JsonResponse({"name": project.name, "id": project.id, "liked": liked, "added": added, 'likes': project.user_liked.count(), "pending": project.pending})

def user(request):
    projects = Project.objects.filter(pending=True)
    return render(request, "skillmatch/user.html", {"pending_projects": projects})

skills = [{"name": "Create", "icon": '<i class="fa-solid fa-hammer"></i>'}, {"name": "Develop", "icon": '<i class="fa-solid fa-layer-group"></i>'}, {"name": "Experiment", "icon": '<i class="fa-solid fa-flask"></i>'}, {"name": "Test", "icon": '<i class="fa-solid fa-vial-circle-check"></i>'}]
def homepage(request):
    return render(request, "skillmatch/homepage.html", {"skills": skills})

def project(request, id):
    return render(request, "skillmatch/project.html", {"project": Project.objects.get(id=id)})

def index(request):
    if not request.user.is_authenticated: return HttpResponseRedirect(reverse("homepage"))
    return render(request, "skillmatch/index.html")

@login_required
@require_POST
def add_project(request, id):
    project = Project.objects.get(pk=id)
    if project in request.user.saved_projects.all():
        request.user.saved_projects.remove(project)
        added = False
    else:
        request.user.saved_projects.add(project)
        added = True
    return JsonResponse({'added': added})

@login_required
def update_likes(request, id):
    project = Project.objects.get(pk=id)
    if project in request.user.liked_projects.all():
        request.user.liked_projects.remove(project)
        liked = False
    else:
        request.user.liked_projects.add(project)
        liked = True
    return JsonResponse({'likes': project.user_liked.count(), "liked": liked})

def image_view(request, url):
    image_url = "images/" + str(url)
    return serve(request, image_url, document_root=settings.MEDIA_ROOT)

fields = ["mechanic", "scientific", "persuasive", "artistic", "calculus"]
def projects_view(request):
    projects = []
    for project in Project.objects.filter(pending=False):
        curProject = {"name": project.name, "id": project.id, "mechanic": project.mechanic, "scientific": project.scientific, "persuasive": project.persuasive, "artistic": project.artistic, "calculus": project.calculus, "introduction": project.introduction}
        if project.image:
            curProject["img"] = project.image.url
        else:
            curProject["img"] = ""
        curProject["abilities"], curProject["careers"] = [],[]
        
        for ability in project.abilities.all(): curProject["abilities"].append(ability.ability.title())
        for career in project.careers.all(): curProject["careers"].append(career.career.title())
        
        projects.append(curProject)

    if request.user.done_test:
        curUser = request.user
        user = np.array([curUser.mechanic, curUser.scientific, curUser.persuasive, curUser.artistic, curUser.calculus])
        for project in projects:
            project_array = np.array([float(project[field]) for field in fields])
            
            cosine = np.dot(user, project_array) / (norm(user)*norm(project_array))
            project["cosine"] = cosine
        projects = sorted(projects, key=lambda d: d['cosine']) 
        
    else:
        shuffle(projects)
    return JsonResponse({"projects": projects}, json_dumps_params={'ensure_ascii': False}, charset='utf-8')


@login_required
def test_view(request):
    test = []
    activity_groups = ActivityGroup.objects.filter(test_id=1).count() # ID = 1 -> Kuder Test
    
    for i in range(1, activity_groups + 1):
        activities = Activity.objects.filter(activity_group_id=i)   
        activities_list = []
        activity_dict = {}
        for activity in activities:
            positive, negative = points(activity.positive.all(), activity.negative.all())
            activity_dict = {
                "positive": [element[0] for element in positive],
                "instruction": activity.activity,
                "negative": [element[0] for element in negative],
                "id": activity.id
            }
            activities_list.append(activity_dict)
        test.append(activities_list)
        
    return JsonResponse({"test": test}, json_dumps_params={'ensure_ascii': False}, charset='utf-8')

# Returns two values list from the positive and negative areas that an activity has
def points(positive, negative):
    return positive.values_list("name"), negative.values_list("name")

def test(request):
    if request.method == "POST":
        areas = json.loads(request.body).get("areas", [])
         
        user = User.objects.get(id=request.user.id)
        total = sum(areas.values())
        for field in ["mechanic", "scientific", "persuasive", "artistic", "calculus"]:
            setattr(user, field, areas[field] / total)
        user.done_test = True
        user.save()
        
        return JsonResponse({'success': True})
        
    return render(request, "skillmatch/test.html")


def authentication(request, form="login"):
    if request.user.is_authenticated: return HttpResponseRedirect(reverse("index"))
    return render(request, "skillmatch/authentication.html", {"sign_up": SignupForm(), "log_in": LoginForm(), "form": form})

def login_view(request):
    if request.user.is_authenticated: return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        form = LoginForm(request.POST)
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "skillmatch/authentication.html", { 
                            "log_in": form, "sign_up": SignupForm(), 
                            "login_message": "LOGIN ERROR: Make sure you entered the right password and username" 
                        })
    return HttpResponseRedirect(reverse("index"))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("authentication", kwargs={"form": "login"}))

def register(request):
    if request.user.is_authenticated: return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        user_type = request.POST["user_type"]
        form = SignupForm(request.POST)

        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            return render(request, "skillmatch/authentication.html", {
                "register_message": "Passwords must match.",
                "sign_up": form,
                "log_in": LoginForm()
            })

        # Attempt to create new user
        try:
            print(user_type)
            if user_type == "student":
                user = Student.objects.create_user(username=username, user_type=user_type, password=password)
                user.save()
            elif user_type == "teacher":
                user = Teacher.objects.create_user(username=username, user_type=user_type, password=password)
                user.save()
        except IntegrityError:
            return render(request, "skillmatch/authentication.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseRedirect(reverse("index"))

