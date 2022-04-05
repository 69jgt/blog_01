from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog_app'

# urlpatterns = [
#     # post views
#     path('', views.post_list, name='post_list'),
#     path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
#     path('<int:post_id>/share/', views.post_share, name='post_share'),
#     path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
#     path('feed/', LatestPostsFeed(), name='post_feed'),
#     path('search/', views.post_search, name='post_search'),
#     path('contact/', views.post_contact,  name='post_contact'),
#     path('about/', views.post_about, name='post_about'),

# ]

urlpatterns = [
#     # post views
      path('', views.main, name='main'),
      path('search/', views.post_search, name='post_search'),
      path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
      path('<int:post_id>/share/', views.post_share, name='post_share'),
      path('tag/<slug:tag_slug>/', views.main, name='post_list_by_tag'),
      # path('post_list/', views.post_list, name='post_list'),
      path('post_list/', views.PostListView.as_view(), name='post_list'),
      path('contact/', views.post_contact,  name='post_contact'),
      path('feed/', LatestPostsFeed(), name='post_feed'),
]

# path('', views.PostListView.as_view(), name='post_list'), # Podemos usar la clase PostListView en vez de la función