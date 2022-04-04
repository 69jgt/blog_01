from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .models import Post, Comment, About
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.conf import settings
from django.contrib import messages



# Test new html
# def test(request):
#     return render(request, 'base.html')

def main(request, tag_slug = None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in = [tag])

    # Pagination section
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'base.html', {'page': page, 'posts': posts, 'tag': tag})

def post_list(request, tag_slug = None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in = [tag])

    # Pagination section
    paginator = Paginator(object_list, 4)  # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    return render(request,
                  'blog/post_list.html', {'page': page, 'posts': posts, 'tag': tag})

# Esta clase es equivalente a la función post_list, con menos código conseguimos el mismo resultado
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug = post,
                             status = 'published',
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)

    # List of active comments for this post
    comments = post.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit = False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids) \
        .exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id = post_id, status = 'published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['nombre']} recomendamos que leas {post.title}"
            message = f"Lee {post.title} en {post_url}\n\n" \
                      f"{cd['nombre']} dice: {cd['comentario']}"
            send_mail(subject, message, 'tutmotsis69@gmail.com', [cd['para']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


# Buscador basado en Postgres

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']

            # Con esta búsqueda se da más relevancia a los resultados encontrados en el título que en el cuerpo
            search_vector = SearchVector('title', weight='A') + \
                SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

            # A trigram is a group of three consecutive characters.
            # You can measure the similarity of two strings by counting the number of trigrams that they share.
            # results = Post.published.annotate(
            #     similarity = TrigramSimilarity('title', query),
            # ).filter(similarity__gt = 0.1).order_by('-similarity')

    return render(request,
                  'blog/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


# Formulario de contacto

def post_contact(request):
    if request.method == "POST":
        subject = request.POST["asunto"]
        message = request.POST["mensaje"] + "\n" + "Correo del usuario: " + request.POST["email"]
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ["tutmotsis69@gmail.com"]
        try:

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Muchas gracias, mensaje enviado correctamente.")
        # return render(request, 'blog/post/contact.html')

        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('blog/post/list.html')

    return render(request, 'blog/post/contact.html')


# Página sobre mi

def post_about(request):
    about = get_object_or_404(About)
    return render(request, 'blog/post/about.html', {'about': about})


