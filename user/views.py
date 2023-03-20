from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Association
from actualite.models import Post
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, When, Value, CharField


def accueil(request):
    posts = Post.objects.all()
    assos = Association.objects.all()
    # if search_query:
    #     posts_search = Post.objects.filter(Q(title__incontains = search_query)|Q(title__areaHash__incontains = search_query))
    context = {
        'posts': posts,
        'assos': assos,
        # 'posts':posts_search,
    }
    return render(request, 'userTests/accueil.html', context)

# login


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(
                request, 'Veuillez fournir un e-mail et un mot de passe valides.')
            return redirect('user_login')

        user = authenticate(request, username=email, password=password)
        # print(email)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(
                request, 'Les informations d\'identification fournies ne sont pas valides.')
            return redirect('user_login')

    return render(request, 'userTests/user_login.html', {})


# register
def sing_up(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        numero = request.POST.get('contact', None)
        address = request.POST.get('address', None)
        docRecepiss = request.FILES['docRecepiss']
        activitePrincipal = request.POST.get('activitePrincipal', None)
        if activitePrincipal:
            activitePrincipal = activitePrincipal.split(",")
        activiteSecondaire = request.POST.get('activiteSecondaire', None)
        if activiteSecondaire:
            activiteSecondaire = activiteSecondaire.split(",")
        activiteThird = request.POST.get('activiteThird', None)
        if activiteThird:
            activiteThird = activiteThird.split(",")
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

        print(activitePrincipal)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"

            # register
        if error == False:
            # Create user and association objects
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            association = Association.objects.create(
                user=user,
                email=email,
                numero=numero,
                address=address,
                docRecepiss=docRecepiss,
                activitePrincipal=activitePrincipal,
                activiteSecondaire=activiteSecondaire,
                activiteThird=activiteThird
            )

            # Login user
            auth_user = authenticate(request, username=name, password=password)
            login(request, auth_user)
            return redirect('accueil')

    context = {
        'error': error,
        'message': message
    }
    return render(request, 'userTests/register.html', context)


# deconnexion
def log_out(request):
    logout(request)
    return redirect('accueil')


# Affichage actualite
def news(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,

    }
    return render(request, 'userTests/news.html', {})


# Ajouter actualite

@login_required(login_url='/user_login')
def getNews(request):
    author = request.user
    posts = Post
    if request.method == "POST":
        title = request.POST['titre']
        text = request.POST['text']
        thumbnail = request.FILES['thumbnail']

        posts = Post.objects.create(
            title=title, text=text, thumbnail=thumbnail, author=author)

        posts.save()

    return redirect('/')


# supprimer actualite @login_required(login_url='/login')
@login_required(login_url='/user_login')
def actu_delete(request, posts_id):
    posts_id = int(posts_id)
    try:
        posts = Post.objects.get(id=posts_id)
    except Post.DoesNotExist:
        return redirect('accueil')
    posts.delete()
    return redirect('accueil')


# @login_required(login_url='/user_login')
# def deleteConfirm(request, post_id):
#     post = Post.objects.get(id=post_id)
#     context = {'post': post}
#     if request.method == "POST":
#         post.delete()
#         return redirect('accueil')
#     return render(request, 'accueil', context)


@login_required(login_url='/user_login')
def update(request, post_id):
    posts = Post.objects.get(id=post_id)
    context = {
        'posts': posts, }

    return render(request, 'userTests/updateActu.html', context)


@login_required(login_url='/user_login')
def updateActu(request, post_id):
    post_id = int(post_id)
    posts = Post.objects.get(id=post_id)

    if request.method == 'POST':
        title = request.POST['titre']
        text = request.POST['text']
        posts.title = title
        posts.text = text
        posts.save()
        return redirect('accueil')

    context = {
        'posts': posts,
    }
    return render(request, 'userTests/accueil.html', context)


# Search Bar
# def searchEtiquette(request):
#     etiquette = request.GET.get('search')
#     result = Association.objects.filter(Q(activitePrincipal__icontains=etiquette) & Q(
#         activiteSecondaire__icontains=etiquette) & Q(activiteThird__icontains=etiquette)).order_by('-activitePrincipal', '-activiteSecondaire', '-activiteThird')

def searchEtiquette(request):
    etiquette = request.GET.get('search')
    result = Association.objects.filter(Q(activitePrincipal__icontains=etiquette) | Q(
        activiteSecondaire__icontains=etiquette) | Q(activiteThird__icontains=etiquette)).annotate(
        priority=Case(
            When(activitePrincipal__icontains=etiquette, then=Value(1)),
            When(activiteSecondaire__icontains=etiquette, then=Value(2)),
            When(activiteThird__icontains=etiquette, then=Value(3)),
            output_field=CharField(),
        )).order_by('priority')
    context = {
        'etiquette': etiquette,
        'result': result
    }
    return render(request, 'userTests/searchView.html', context)
