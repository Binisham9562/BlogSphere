from django.contrib import admin
from .models import Category
from blogapp.models import Post
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.sites.models import Site

class CategoryAbstractAdmin(admin.ModelAdmin):

    exclude=['created_user']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    # prepopulated_fields = {'slug': ('category_name',)}
     # Automatically populate the slug from the name

admin.site.register(Category, CategoryAdmin)

class UserAdmin(admin.ModelAdmin):
    # Disable the Add button
    def has_add_permission(self, request):
        return False
    
    # # Disable the Delete button
    # def has_delete_permission(self, request, obj=None):
    #     return False

class PostAdmin(admin.ModelAdmin):
    # Disable the Add button
    # def has_add_permission(self, request):
    #     return False
    
    # # Disable the Delete button
    # def has_delete_permission(self, request, obj=None):
    #     return False
    pass



# Unregister the Site model to remove it from the admin panel
admin.site.unregister(Site)
admin.site.unregister(User)  # Unregister the default User admin if already registered
admin.site.register(User, UserAdmin)  # Register with custom admin
admin.site.register(Post, PostAdmin)
