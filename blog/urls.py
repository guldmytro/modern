from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.archive_blog, name="archive_blog"),
    path('category/<tag>', views.blog_by_tag, name="blog_by_tag"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name="post_detail"),
    path('search/', views.search, name="search"),
    path('comment/', views.leave_comment, name="comment")

]