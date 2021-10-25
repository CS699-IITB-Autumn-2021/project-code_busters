#from types import ClassMethodDescriptorType
from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

from .models import *
# Register your models here.
from .models import NewUser
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff','image')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name','image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name','image', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
class UpvoteAdmin(admin.ModelAdmin):
    list_display=('reply','user')

class DownvoteAdmin(admin.ModelAdmin):
    list_display=('reply','user')

class LikeAdmin(admin.ModelAdmin):
    list_display=('question','user')

class DislikeAdmin(admin.ModelAdmin):
    list_display=('question','user')

admin.site.register(NewUser,UserAdminConfig)

admin.site.register(Tag)
admin.site.register(Hobby)
admin.site.register(Save)
admin.site.register(Notify)

admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(UpVote,UpvoteAdmin)
admin.site.register(DownVote, DownvoteAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)