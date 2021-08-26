from django.shortcuts import render
from django.http import JsonResponse
from blog import utils
from .models import About
from blog.common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def index(request):
    latest_posts = utils.get_latest_posts()
    tags = utils.get_tags()
    random_article = utils.get_random_article()
    context = {
        'latest_posts': latest_posts,
        'tags': tags,
        'random_article': random_article
    }
    return render(request, 'pages/index.html', context)


def about(request):
    post = About.objects.last()
    context = {
        'post_type': 'about',
        'page': post,
        'page_name': 'Об авторе',
    }
    return render(request, 'pages/about.html', context)


def feadback(request):
    context = {
        'post_type': 'feadback',
        'page_name': 'Обратная связь',
    }
    return render(request, 'pages/feadback.html', context)


@ajax_required
@require_POST
def send_message(request):
    context = {
        'name': request.POST.get('name'),
        'email': request.POST.get('email'),
        'msg': request.POST.get('comment')
    }
    message = render_to_string('email/letter.html', context)
    post = About.objects.last()
    if post.email:
        em = EmailMessage(subject='Новое сообщение с сайта',
                          body=message,
                          to=[post.email],
                          headers={'content-type': 'text/html'}
                          )
    try:
        em.send()
        return JsonResponse({'status': 'ok'})
    except:
        return JsonResponse({'status': 'bad'})

