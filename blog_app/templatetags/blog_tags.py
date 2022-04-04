from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/trend.html')
def show_trend(count=5):
    trend = Post.published.order_by('-publish')[:count]
    return {'trend': trend}

@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/slides.html')
def show_slides(count=5):
    slides = Post.published.order_by('publish')[:count]
    return {'slides': slides}

@register.inclusion_tag('blog/older_posts.html')
def show_older(count=6):
    older = Post.published.order_by('publish')[:count]
    return {'older': older}


# @register.inclusion_tag('blog/posts_list.html')
# def show_list(all):
#     post_list = Post.published.order_by('publish')
#     return {'post_list': post_list}


# Markdown is a plain-text formatting syntax
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

