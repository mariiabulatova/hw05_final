from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # 1 Главная страница (ВСЕМ)
    path('', views.index, name='index'),
    # 2 Отображение всех записей группы (ВСЕМ)
    path('group/<str:slug>/', views.group_posts, name='group_list'),
    # 3 Профайл пользователя (ВСЕМ)
    path('profile/<str:username>/', views.profile, name='profile'),
    # 4 Просмотр записи (ВСЕМ)
    path('posts/<int:post_id>/', views.post_view, name='post_detail'),
    # 5 Редактирование записи (АВТОРУ)
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # 6 Создание нового поста (АВТОРИЗОВАННОМУ)
    path('create/', views.post_create, name='post_create'),
    # 7 Комментирование поста
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),
    # 8
    path(
        'follow/',
        views.follow_index,
        name='follow_index'),
    # 9
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    # 10
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
]
