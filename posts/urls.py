from django.urls import path
from . import views

urlpatterns = [
    path("group/<slug>/", views.group_posts, name="group_posts"),
    path("new/", views.new_post, name="new_post"),
    path("", views.index, name="index"),

    # просмотр записи
    path('<username>/<int:post_id>/', views.post_view, name='post'),

    # редактирование записи
    path('<username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),

]