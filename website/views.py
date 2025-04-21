from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddPostForm
from .models import Post


def home(request):
    if request.user.is_authenticated:
        # Mostrar solo las publicaciones del usuario autenticado
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
    else:
        posts = None

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'posts': posts})


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
	messages.success(request, "You Have Been Logged Out...")
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
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})



# def customer_record(request, pk):
# 	if request.user.is_authenticated:
# 		# Look Up Records
# 		customer_record = Record.objects.get(id=pk)
# 		return render(request, 'record.html', {'customer_record':customer_record})
# 	else:
# 		messages.success(request, "You Must Be Logged In To View That Page...")
# 		return redirect('home')



# def delete_record(request, pk):
# 	if request.user.is_authenticated:
# 		delete_it = Record.objects.get(id=pk)
# 		delete_it.delete()
# 		messages.success(request, "Record Deleted Successfully...")
# 		return redirect('home')
# 	else:
# 		messages.success(request, "You Must Be Logged In To Do That...")
# 		return redirect('home')


# def add_record(request):
# 	form = AddRecordForm(request.POST or None)
# 	if request.user.is_authenticated:
# 		if request.method == "POST":
# 			if form.is_valid():
# 				add_record = form.save()
# 				messages.success(request, "Record Added...")
# 				return redirect('home')
# 		return render(request, 'add_record.html', {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In...")
# 		return redirect('home')


# def update_record(request, pk):
# 	if request.user.is_authenticated:
# 		current_record = Record.objects.get(id=pk)
# 		form = AddRecordForm(request.POST or None, instance=current_record)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, "Record Has Been Updated!")
# 			return redirect('home')
# 		return render(request, 'update_record.html', {'form':form})
# 	else:
# 		messages.success(request, "You Must Be Logged In...")
# 		return redirect('home')

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