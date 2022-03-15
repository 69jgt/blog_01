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

@register.inclusion_tag('blog/slides.html')
def show_slides(count=5):
    slides = Post.published.order_by('publish')[:count]
    return {'slides': slides}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


# Markdown is a plain-text formatting syntax
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))