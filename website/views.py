from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddPostForm
from .models import Post
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship
from itertools import chain


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.error(request, "Ya has enviado una solicitud a este usuario.")
    elif Friendship.objects.filter(user1=request.user, user2=to_user).exists() or Friendship.objects.filter(user1=to_user, user2=request.user).exists():
        messages.error(request, "Ya eres amigo de este usuario.")
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, "Solicitud de amistad enviada.")
    return redirect('home')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
    friend_request.delete()
    messages.success(request, "Solicitud de amistad aceptada.")
    return redirect('home')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    messages.success(request, "Solicitud de amistad rechazada.")
    return redirect('home')

@login_required
def home(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    users = User.objects.exclude(id=request.user.id)  # Excluir al usuario actual

    # Obtener amigos del usuario
    friends_user1 = Friendship.objects.filter(user1=request.user).values_list('user2', flat=True)
    friends_user2 = Friendship.objects.filter(user2=request.user).values_list('user1', flat=True)
    friends = set(chain(friends_user1, friends_user2))  # Combinar ambos conjuntos de amigos

    # Excluir amigos actuales de la lista de usuarios
    users = users.exclude(id__in=friends)

    # Obtener solicitudes de amistad recibidas
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    return render(request, 'home.html', {
        'posts': posts,
        'users': users,
        'friend_requests': friend_requests,
    })

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    return render(request, 'login.html')

def logout_user(request):
	logout(request)
	messages.success(request, "Has cerrado sesión.")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "Te has registrado con éxito")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


@login_required
def view_posts(request):
    # Mostrar solo los posts del usuario autenticado
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'view_posts.html', {'posts': user_posts})

@login_required
def create_post(request):
    # Crear un nuevo post
    form = AddPostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user  # Asociar el post al usuario autenticado
            new_post.save()
            messages.success(request, "Post creado exitosamente.")
            return redirect('view_posts')
    return render(request, 'create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    # Modificar un post propio
    post = get_object_or_404(Post, pk=pk, user=request.user)  # Asegurarse de que el post pertenece al usuario
    form = AddPostForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Post actualizado exitosamente.")
            return redirect('view_posts')
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    # Eliminar un post propio
    post = get_object_or_404(Post, pk=pk, user=request.user)  # Asegurarse de que el post pertenece al usuario
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post eliminado exitosamente.")
        return redirect('view_posts')
    return render(request, 'delete_post.html', {'post': post})