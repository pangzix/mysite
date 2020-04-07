from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from comment.models import Comment

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    else:
        search = ''
        article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list,6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles,'search':search}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = get_object_or_404(ArticlePost,id=id)
    comments = Comment.objects.filter(article=id)
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
    article.body = md.convert(article.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    article.toc = m.group(1) if m is not None else ''
    context = {'article':article,'comments':comments}
    return render(request,'article/detail.html',context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("error")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form':article_post_form}
        return render(request,'article/create.html',context)

def article_safe_detete(request,id):
    if request.method == 'POST':

        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("error")


def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail" ,id=id)
        else:
            return HttpResponse("error")

    else:
        article_post_form = ArticlePostForm()
        context = {'article':article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)




