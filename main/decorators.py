import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from posts.models import Post


def allow_self(function): #passed like delte,draft & edit_post
    def wrapper(request, *args, **kwargs): #complete arguments called
        id = kwargs["id"]
        if not Post.objects.filter(id=id,author__user=request.user).exists():
            #conditionally check it is normal http request or ajax request (edit=link) (create =ajax)
            if request.headers.get("x-requested-with") == "XMLHttpRequest": #ajax
                response_data = {
                    "status": "error",
                    "title": "Unauthorized access",
                    "message": "Unauthorized access",
                }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else: #
                return HttpResponseRedirect(reverse("web:index")) #can implement page showing error

        return function(request, *args, **kwargs)

    return wrapper
        