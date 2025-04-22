from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario

class Post(models.Model):  # Cambia el nombre del modelo a "Post"
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Cambia los campos para reflejar contenido de publicaciones

    def __str__(self):
        return f"{self.content} - {self.user.username}"  # Muestra el título y el usuario

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}"

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"