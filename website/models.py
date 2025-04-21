from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de usuario

class Post(models.Model):  # Cambia el nombre del modelo a "Post"
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Cambia los campos para reflejar contenido de publicaciones

    def __str__(self):
        return f"{self.content} - {self.user.username}"  # Muestra el título y el usuario