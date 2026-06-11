import datetime
import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from main.functions import paginate_instances
from main.decorators import allow_self

from posts.forms import PostForm
from posts.models import Author, Category, Post


# Create your views here.
@login_required(login_url= "/users/login/")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            tags = form.cleaned_data['tags']

            if not Author.objects.filter(user=request.user).exists():
                author = Author.objects.create(user=request.user,name=request.user.username)
            else:
                author = request.user.author # onetoone firld ayath kond user authorine villikan pattum

            instance = form.save(commit = False)
            instance.published_date = datetime.date.today()
            # instance.published_date = datetime.date.strftime("%Y-%m-%d")
            instance.author =  author
            instance.save()    

            tags_list = tags.split(",")   # split on comma and remove empty tags   
            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title" : "Successfully Submitted",
                "message" : "Successfully Submitted",
                "status" : "success",
                "redirect" : "yes",
                "redirect_url" : "/"
            }

            return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        data = {
            "title": "Hello",
            "description": "Hello",
            "short_description": "Hello",
            "time_to_read": "Hello",
            "tags": "Technology,programming,coding"
        }
        form = PostForm(initial = data)
        context = {
            "title": "Create new Post",
            "form": form,
        }
        return render(request, "posts/create.html", context=context)


@login_required(login_url="/users/login")
def my_posts(request):
    posts = Post.objects.filter(author__user=request.user, is_deleted=False)
    instances = paginate_instances(request,posts, per_page=1)
    context = {
        "title": "My Posts",
        "instances": instances,
        "posts": posts      
    }
    return render(request, "posts/my-posts.html",context=context)


@login_required(login_url="/users/login")
@allow_self
def delete_post(request,id):
    instance = get_object_or_404(Post, id=id)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "title" : "Deleted Successfully",
        "message" : "Post Deleted Successfully",
        "status" : "success"
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/users/login")
@allow_self
def draft_post(request,id):
    instance = get_object_or_404(Post, id=id)
    instance.is_draft = not instance.is_draft
    instance.save()

    response_data = {
        "title" : "Successfully Changed",
        "message" : "Post Updated Successfully",
        "status" : "success"
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url= "/users/login/")
@allow_self
def edit_post(request,id): #need id for a post to edit
    Post.objects.filter(id=id,author__user=request.user)
    instance = get_object_or_404(Post, id=id) #get current post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=instance) #then only it know edit form
        if form.is_valid():

            tags = form.cleaned_data['tags']

            #already author undavum


            instance = form.save(commit = False)
            instance.save()    

            instance.categories.clear() #clear all categories from category 


            tags_list = tags.split(",")   # split on comma and remove empty tags   
            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.categories.add(category)

            response_data = {
                "title" : "Successfully Submitted",
                "message" : "Successfully Submitted",
                "status" : "success",
                "redirect" : "yes",
                "redirect_url" : "/"
            }

            return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        category_string = ""
        for category in instance.categories.all(): #tags is manytomany field
            category_string += f"{category.title},"

        form = PostForm(instance=instance, initial={"tags":category_string[:-1]}) #instance passed, form knows he comes to edit current post :-1 last comma
        context = {
            "title": "Create new Post",
            "form": form,
        }
        return render(request, "posts/create.html", context=context)