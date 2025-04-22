from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('accounts/login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
        # Rutas para las acciones sobre los posts
    path('posts/', views.view_posts, name='view_posts'),  # Ver los posts propios
    path('posts/create/', views.create_post, name='create_post'),  # Crear un nuevo post
    path('posts/update/<int:pk>/', views.update_post, name='update_post'),  # Modificar un post propio
    path('posts/delete/<int:pk>/', views.delete_post, name='delete_post'),  # Eliminar un post propio
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
