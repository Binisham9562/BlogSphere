from django.urls import path
from .views import post_list, create_post, post_detail, edit_post, delete_post, like_post, dislike_post,category_posts,search_posts,user_profile


urlpatterns = [
    path('', post_list, name='post_list'),
    path('category/<int:category_id>/', category_posts, name='category_posts'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('search/', search_posts, name='search_posts'),
    path('profile/',user_profile, name='user_profile'),
    path('post/edit/<int:category_id>/<int:post_id>/',edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', dislike_post, name='dislike_post'),
]
