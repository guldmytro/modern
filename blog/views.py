from django.shortcuts import render, get_object_or_404
from .models import Post, Tag
from comments.models import Comment
from . import utils
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .common.decorators import ajax_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def archive_blog(request):
    tags = utils.get_tags()
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 16)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_posts = utils.get_latest_posts()
    context = {
        'page': page,
        'posts': posts,
        'page_name': 'Статьи',
        'post_type': 'archive',
        'tags': tags,
        'current_tag': None,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/archive.html', context)


def blog_by_tag(request, tag):
    current_tag = Tag.objects.get(slug=tag)
    tags = utils.get_tags()
    posts_list = Post.published.filter(category__slug=tag)
    paginator = Paginator(posts_list, 16)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_posts = utils.get_latest_posts()
    context = {
        'page': page,
        'posts': posts,
        'page_name': current_tag.title,
        'post_type': 'archive',
        'tags': tags,
        'current_tag': tag,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/archive.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    comments = Comment.published.filter(post__pk=post.pk).order_by('publish')
    related_posts = False
    try:
        related_posts = Post.published.filter(category=post.category).exclude(pk=post.pk).order_by('-publish')[:10]
    except:
        pass

    context = {
        'post': post,
        'page_name': post.title,
        'post_type': 'single',
        'comments': comments,
        'related_posts': related_posts
    }
    return render(request, 'blog/single.html', context)


@ajax_required
@require_POST
def leave_comment(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    msg = request.POST.get('msg')
    reply = request.POST.get('reply')
    post = Post.objects.get(pk=int(request.POST.get('post')))
    if not name or not surname or not msg or not post:
        return JsonResponse({'status': 'error'})

    comment = Comment()
    comment.name = name
    comment.surname = surname
    comment.comment = msg
    comment.post = post

    replied_comment = False

    try:
        replied_comment = Comment.objects.get(pk=int(reply))
    except:
        pass

    if replied_comment:
        comment.reply = replied_comment

    comment.save()

    if comment.pk:
        response = {
            'status': 'ok',
            'data': {
                'id': comment.pk,
                'msg': comment.comment,
                'full_name': comment.full_name(),
                'time': comment.publish,
            }
        }
        if replied_comment:
            response['data']['replied_comment'] = {
                'id': replied_comment.pk,
                'msg': replied_comment.comment,
                'time': replied_comment.publish,
                'full_name': replied_comment.full_name()
            }
        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error'})


def search(request):

    search_header = None
    if 'query' in request.GET:
        query = request.GET['query']
        search_header = f'Результаты поиска: <em>"{query}"</em>'
        search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
        search_query = SearchQuery(query)
        latest_posts = Post.published.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    else:
        latest_posts = Post.published.all()[:4]

    context = {
        'page_name': 'Поиск',
        'post_type': 'archive',
        'current_tag': None,
        'latest_posts': latest_posts,
        'search_header': search_header,
    }
    return render(request, 'blog/search.html', context)
