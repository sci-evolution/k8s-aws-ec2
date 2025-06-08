import re, json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .services import UserService
from .exceptions import NotFound


TITLE: str = "Users"

def json_decode(user_json: str) -> dict[str, any]:
    user = json.loads(user_json)
    user["age"] = int(user["age"]) if user["age"] else None
    user["joined_at"] = user["joined_at"] or None
    is_active = True if user["is_active"] else False
    user["is_active"] = is_active
    return user

def new_user(request):
    try:
        template = loader.get_template("users/create.html")
        context = { "title" : TITLE}
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

def get_all(request):
    try:
        users = UserService().get_all()
        template = loader.get_template("users/index.html")
        context = {
            "title": TITLE,
            "users": users
        }
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

def get_by_params(request):
    try:
        params = request.GET.get("search")
        pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-.\s]{1,48}[a-zA-Z0-9]$")
        
        if(not pattern.match(params)):
            return HttpResponseBadRequest("Invalid search")
        
        users = UserService().get_by_params(params)
        template = loader.get_template("users/index.html")
        context = {
            "title": TITLE,
            "users": users
        }
        return HttpResponse(template.render(context, request))
    except Exception as err:
        print(err)
        raise

###############################################################################
from .interfaces import IViewGetById, IServiceGetById

class UserView(IViewGetById):
    def get_by_id(self, request, user_id, IServiceGetById = UserService()):
        try:
            user = IServiceGetById.get_by_id(user_id)
            template = loader.get_template("users/retrieve.html")
            context = {
                "title": TITLE,
                "user": user
            }
            return HttpResponse(template.render(context, request))
        except NotFound as err404:
            print(err404)
            raise Http404("User not found!") from err404
        except Exception as err:
            print(err)
            raise

###############################################################################

def create(request):
    try:
        user = json_decode(request.body)
        if(UserService().create(user)):
            return HttpResponseRedirect(reverse("users:index",))
    except Exception as err:
        print(err)
        raise

def update(request, user_id):
    user = json_decode(request.body)
    user["user_id"] = user_id
    
    try:
        if(UserService().update(user)):
            return HttpResponseRedirect(reverse("users:retrieve", args=[user["user_id"]]))
    except NotFound as err404:
        print(err404)
        raise Http404("User not found!") from err404
    except Exception as err:
        print(err)
        raise

def delete(request, user_id):
    try:
        if(UserService().delete(user_id)):
            return HttpResponseRedirect(reverse("users:index",))
    except NotFound as err404:
        print(err404)
        raise Http404("User not found!") from err404
    except Exception as err:
        print(err)
        raise
