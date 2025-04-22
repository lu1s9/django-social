from django.contrib import admin
from .models import Post, Comment, Friendship, FriendRequest

admin.site.register(Post)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Comment)