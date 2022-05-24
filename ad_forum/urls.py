from django.conf.urls.static import static
from django.urls import path

from coursework import settings
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('news/', NewsPage.as_view(), name='news'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('posts/', PostsPage.as_view(), name='all_posts'),
    path('post/<int:post_id>/', get_post_by_id, name='one_post'),
    path('search/', search, name='search'),
    path('check_search_bar/', check_search_bar, name='check_search_bar'),

    path('reviews/<int:posts_id>/', get_reviews, name='reviews'),
    path('add_like_review/<int:review_id>/', add_like_review, name='add_like_review'),
    path('add_dislike_review/<int:review_id>/', add_dislike_review, name='add_dislike_review'),
    path('add_review/<int:posts_id>/', add_review, name='add_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)