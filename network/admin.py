from django.contrib import admin
from .models import User, Post, Follow, Comment, Reaction


# Register your models here.
class PostAdminInline(admin.TabularInline):
    model = Post
    extra = 1

class CommentAdminInline(admin.TabularInline):
    model = Comment
    extra = 1

class FollowAdminInline(admin.TabularInline):
    model = Follow
    fk_name = "to_person"
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = (PostAdminInline, CommentAdminInline, )

class ReactionAdminInline(admin.TabularInline):
    model = Reaction
    fk_name = "to_post"
    extra = 1
    
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Reaction)
