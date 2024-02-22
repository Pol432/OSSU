from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

AREAS = [("mechanic", "Mecánico"),
         ("scientific", "Científico"),
         ("persuasive", "Persuasivo"),
         ("artistic", "Artístico"),
         ("calculus", "Cálculo")]

class User(AbstractUser):
    done_test = models.BooleanField(default=False)
    
    mechanic = models.FloatField(null=True)
    scientific = models.FloatField(null=True)
    persuasive = models.FloatField(null=True)
    artistic = models.FloatField(null=True)
    calculus = models.FloatField(null=True)
    
    saved_projects = models.ManyToManyField("Project", related_name="user_pendings", blank=True)
    liked_projects = models.ManyToManyField("Project", related_name="user_liked", blank=True)
    user_type = models.CharField(choices=[("student", "student"), ("teacher", "teacher"), ("admin", "admin")], max_length=8)


class Student(User):
    onprogress_projects = models.ManyToManyField("Project", related_name="user_onprogress")
    previous_projects = models.ManyToManyField("Project", related_name="user_previous")


class Teacher(User):
    created_projects = models.ManyToManyField("Project", related_name="creator")


class ProjectRating(models.Model):
    rating = models.FloatField()
    user = models.ForeignKey("Teacher", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_rating")


class Project(models.Model):
    name = models.CharField(max_length=50)
    careers = models.ManyToManyField("Career", blank=True, related_name="careers")
    abilities = models.ManyToManyField("Ability", blank=True, related_name="abilities")
    introduction = models.TextField()
    instructions = models.TextField()
    courses = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    pending = models.BooleanField(default=False)
    
    mechanic = models.FloatField(null=True)
    scientific = models.FloatField(null=True)
    persuasive = models.FloatField(null=True)
    artistic = models.FloatField(null=True)
    calculus = models.FloatField(null=True)
    
    def __str__(self):
        return f"{self.name}"


class Career(models.Model):
    career = models.CharField(max_length=20)
    def __str__(self): return f"{self.career}"

class Ability(models.Model):
    ability = models.CharField(max_length=20)
    def __str__(self): return f"{self.ability}"

class KuderTest(models.Model):
    name = models.CharField(max_length=100)

class ActivityGroup(models.Model):
    test = models.ForeignKey("KuderTest", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id}"
    
class Activity(models.Model):
    activity = models.CharField(max_length=999)
    
    positive = models.ManyToManyField("InterestArea", related_name="positive_interest")
    negative = models.ManyToManyField("InterestArea", related_name="negative_interest")
    
    activity_group = models.ForeignKey("ActivityGroup", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.activity} ({self.activity_group.id})"
    
class InterestArea(models.Model):
    name = models.CharField(choices=AREAS, max_length=10)
    
    def __str__(self):
        return f"{self.name} ({self.id})"