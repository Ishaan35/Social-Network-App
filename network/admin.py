from django.contrib import admin

from network.models import Like, Post, User, Follower

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
