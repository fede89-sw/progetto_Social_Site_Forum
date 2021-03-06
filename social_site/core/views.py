from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.list import ListView 
from forum.models import Discussione, Sezione, Post

# Create your views here.


class HomeView(ListView):
    """ posso fare solito modo """
    # model = Sezione
    # template_name = "core/homepage.html"
    """ oppure per poter specificare filtri per la queryset o un ordinamento """
    queryset = Sezione.objects.all()[::-1]
    template_name = "core/homepage.html"
    context_object_name = "lista_sezioni"


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = "core/users_list.html"


def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    discussioni_utente = Discussione.objects.filter(autore_discussione=user).order_by("-data_creazione")
    context = {"user": user, "discussioni_utente": discussioni_utente}
    return render(request, "core/user_profile.html", context)


def cerca(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/cerca/")
        discussioni = Discussione.objects.filter(titolo__icontains=querystring)
        posts = Post.objects.filter(contenuto__icontains=querystring)
        users = User.objects.filter(username__icontains=querystring)
        context = {"discussioni":discussioni, "posts":posts, "users":users}
        return render(request, "core/cerca.html", context)
    else:
        return render(request, "core/cerca.html")
