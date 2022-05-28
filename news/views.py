import csv

import xlwt
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView

from .forms import RegisterUserForm, LoginUserForm
from .models import *
from .utils import *


class MainPageView(View):
    template_name = 'ad_forum/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Главная страница',
            'menu': menu,
            'top_posts': set_top_posts(),
        }
        return render(request, 'ad_forum/index.html', context=context)


class NewsPage(ListView):
    model = News
    template_name = 'ad_forum/news.html'
    context_object_name = 'news'
    extra_context = {'title': 'Новости'}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['top_posts'] = set_top_posts()
        return context


class PostsPage(ListView):
    model = Post
    template_name = 'ad_forum/posts.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Публикации'}


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['top_posts'] = set_top_posts()
        return context


class RegisterFormView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    extra_context = {'title': 'Регистрация'}

    template_name = 'ad_forum/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['top_posts'] = set_top_posts()
        return context

    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name = 'auth_users'))
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(LoginView):
    form_class = LoginUserForm
    template_name = 'ad_forum/login.html'
    success_url = reverse_lazy('news')
    extra_context = {'title': 'Логин'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['top_posts'] = set_top_posts()
        return context


def get_reviews(request, posts_id):
    reviews = Review.objects.filter(post_id=posts_id)
    post = Post.objects.get(pk=posts_id)
    reviews_count = Review.objects.filter(post_id=posts_id).count()
    context = {
            "reviews": reviews,
            "reviews_count": reviews_count,
            "title": "Отзывы",
            "menu": menu,
            "top_posts": set_top_posts(),
            "post": post,
        }
    return render(request, "ad_forum/reviews.html", context=context)


def add_like_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.likes_count += 1
    review.save()
    return HttpResponseRedirect('/reviews/' + str(review.post_id.id))


def add_dislike_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.dislikes_count += 1
    review.save()
    return HttpResponseRedirect('/reviews/' + str(review.post_id.id))


def add_review(request, posts_id):
    # Проверяем есть ли у данного пользователя разрешение для добавления поста
    # Если такого разрешения нет, то выкидываем исключение PermissionDenied
    if not request.user.has_perm('ad_forum.add_review'):
        raise PermissionDenied
    review = Review()
    review.text = request.POST.get('review_text')
    review.likes_count = 0
    review.dislikes_count = 0
    review.post_id = Post.objects.get(id=posts_id)
    review.save()

    return HttpResponseRedirect('/reviews/' + str(review.post_id.id))


def logout_user(request):
    logout(request)
    return redirect('login')


def set_top_posts():
    posts = Post.objects.order_by('-rating')
    return posts


def get_post_by_id(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'title': f'{post.name}',
        'menu': menu,
        'top_posts': set_top_posts(),
        'post': post,
    }
    return render(request, "ad_forum/post.html", context=context)


def search(request):
    context = {
        'title': f'Поиск',
        'menu': menu,
        'top_posts': set_top_posts(),
    }
    return render(request, "ad_forum/search.html", context=context)


def check_search_bar(request):
    if request.method == 'GET':
        search_input = request.GET["search_name"]

        post_names = Post.objects.values_list('name', flat=True)
        directors_names = Director.objects.values_list('full_name', flat=True)

        if search_input in post_names:
            post = Post.objects.get(name=search_input)
            context = {
                'title': f'{post.name}',
                'menu': menu,
                'top_posts': set_top_posts(),
                'post': post,
            }
            return HttpResponseRedirect('/post/' + str(post.id))

        elif search_input in directors_names:
            posts = Post.objects.filter(director__full_name=search_input)
            print(posts)
            context = {
                'title': f'Публикации рекламодателя {search_input}',
                'menu': menu,
                'top_posts': set_top_posts(),
                'posts': posts,
            }
            return render(request, "ad_forum/directors_posts.html", context=context)

        else:
            return HttpResponse('Error', content_type='text/html')


def download_news(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="news.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('News')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['ID', 'Title', 'Text']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = News.objects.all().values_list('id', 'title', 'text')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
