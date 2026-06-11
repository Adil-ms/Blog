from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.postgres.search import SearchVector

from main.functions import paginate_instances
from posts.models import Post
from posts.models import Author, Category
 
# Create your views here.
def index(request):
    posts = Post.objects.filter(is_deleted=False,is_draft=False)
    authors = Author.objects.all()
    categories = Category.objects.all()[:5]

    q = request.GET.get('q')
    if q:
        posts = posts.annotate(search=SearchVector("title","author__name","categories__title")).filter(search=q)
        # posts = posts.filter(title__search=q)


    search_authors = request.GET.getlist("author")
    print(search_authors)

    if search_authors:
        posts = posts.filter(author__in=search_authors)

    search_categories = request.GET.getlist("category")
    print(search_categories)

    if search_categories:
        posts = posts.filter(categories__in=search_categories).distinct()

    sort = request.GET.get("sort")
    if sort:
        if sort == "title-asc":
            posts = posts.order_by("title")
        elif sort == "title-desc":
            posts = posts.order_by("-title")
        elif sort == "date-asc":
            posts = posts.order_by("published_date")
        elif sort == "date-desc":
            posts = posts.order_by("-published_date")

    instances = paginate_instances(request,posts)

    numbers = [1,2,3,4,5,6,7,8,9,10]

    context = {
        "title": "HomePage",
        "instances": instances,
        "authors": authors,
        "categories": categories,
        "numbers": numbers
    }
    return render(request, 'web/index.html', context=context)


def post(request,id):
    instance = get_object_or_404(Post.objects.filter(id=id))
    context = {
        "instance": instance
    }
    return render(request, 'web/post.html', context=context)