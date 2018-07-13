from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment, Subscriber
from .forms import CommentForm, TagForm, PostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.template.loader import render_to_string

# There are how many comments/posts on each page
post_paginator = 5
comment_paginator = 5

# Create your views here.
def post_list(request, tag_slug=None):
    list_objects = Post.published.all().order_by('-publish')
    tag = None
    title = 'Blog'

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        list_objects = list_objects.filter(tags__in=[tag])

    paginator = Paginator(list_objects, post_paginator)

    posts = paginator.page(1)

    return render(request, 'blog/list.html', {'posts': posts, 'tag': tag, 'title': title})

def post_list_page(request, page, tag_slug=None):
    list_objects = Post.published.all().order_by('-publish')
    tag = None
    result = {"page": page}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        list_objects = list_objects.filter(tags__in=[tag])

    paginator = Paginator(list_objects, post_paginator)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    data = render_to_string('blog/list_page.html', {'posts': posts})
    result = {"list": data, "page": page}
    return JsonResponse(result)

def draft_post_list(request):
    list_objects = Post.draft.all().order_by('-updated')
    title = 'Drafts'

    paginator = Paginator(list_objects, post_paginator)
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    posts = paginator.page(1)
    return render(request, 'blog/drafts.html', {'posts': posts, 'title': title})

def draft_list_page(request, page):
    list_objects = Post.draft.all().order_by('-updated')
    result = {"page": page}

    paginator = Paginator(list_objects, post_paginator)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    data = render_to_string('blog/draft_list_page.html', {'posts': posts})
    result = {"list": data, "page": page}
    return JsonResponse(result)

def post_detail(request, year, month, day, post, page=None):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    list_comments = post.comments.filter(active=True, parent=None).order_by('-created')
    paginator = Paginator(list_comments, comment_paginator)

    if page:
        comments = paginator.page(page)
    else:
        comments = paginator.page(1)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'year': year, 'month': month, 'day': day, 'similar_posts': similar_posts, 'page': page})

def comment_page(request, year, month, day, post, page):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    list_comments = post.comments.filter(active=True, parent=None).order_by('-created')
    paginator = Paginator(list_comments, comment_paginator)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    text = render_to_string('blog/comment_page.html', {"post": post, "comments": comments})
    result = {"success": text, "page": page}
    return JsonResponse(result)

def post_share(request, year, month, day, post):
    # Retrieve post by id
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    title = 'Share post to friends'

    if request.method == 'POST':
        # Form was submitted
        name = request.POST.get('name')
        email = request.POST.get('email')
        to = request.POST.get('to')
        msg = request.POST.get('message')

        url = "http://www.minalinsky.info" + post.get_absolute_url()
        subject = '{} ({}) recommends you reading "{}"'.format(name, email, post.title)
        message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, url, name, msg)
        try:
            send_mail(subject, message, 'jerry574638690@gmail.com', [to])
            text = 'success'
            result = {"success": text}
        except:
            text = 'failed'
            result = {"failed": text}
        return JsonResponse(result)

    return render(request, 'blog/share.html', {'post': post, 'title': title})

def add_post(request):
    title = 'Write new post'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.save()
            if post_item.status == 'published':
                list_subscriber = Subscriber.objects.all()
                subject = 'New post of Minalinsky\'s blog'
                url = "http://www.minalinsky.info" + post_item.get_absolute_url()
                message = 'A new artical has been posted, check it at: \n {} \n Minalinsky'.format(url)
                for subscribe in list_subscriber:
                    send_mail(subject, message, 'jerry574638690@gmail.com', [subscribe.email])
            return HttpResponseRedirect(reverse('blog:post_list_view'))
    else:
        form = PostForm()
    return render(request, 'blog/addpost.html', {'form': form, 'title': title})

def edit_post(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    title = 'Edit post: '+ str(post.title)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post_item = form.save(commit=False)
        post_item.save()
        if post_item.status == 'published':
            return HttpResponseRedirect(reverse('blog:post_detail_view', args=(year, month, day, post.slug)))
        else:
            return HttpResponseRedirect(reverse('blog:post_list_view'))
    return render(request, 'blog/addpost.html', {'form': form, 'title': title})

def delete_comment(request, year, month, day, post, id):
    comment = get_object_or_404(Comment, id=id)
    comment.active = False
    comment.save()
    return HttpResponseRedirect(reverse('blog:post_detail_view', args=(year, month, day, post)))

def edit_draft(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='draft', updated__year=year, updated__month=month, updated__day=day)
    title = 'Edit post: '+ str(post.title)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post_item = form.save(commit=False)
        post_item.save()
        if post_item.status == 'published':
            list_subscriber = Subscriber.objects.all()
            subject = 'New post of Minalinsky\'s blog'
            url = "http://www.minalinsky.info" + post_item.get_absolute_url()
            message = 'A new artical has been posted, check it at: \n {} \n Minalinsky'.format(url)
            for subscribe in list_subscriber:
                send_mail(subject, message, 'jerry574638690@gmail.com', [subscribe.email])
        return HttpResponseRedirect(reverse('blog:post_list_view'))
    return render(request, 'blog/addpost.html', {'form': form, 'title': title})

def homepage(request):
    title = 'homepage'
    return render(request, 'blog/homepage.html', {"title": title})

def contact(request):
    title = 'Contact the author'

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('message')
        subject = '{} contacts you at your blog'.format(name)
        message = '{} \n from {}'.format(msg, email)
        try:
            send_mail(subject, message, 'jerry574638690@gmail.com', ['jerry574638690@gmail.com'])
            result = {'success': 'success'}
            return JsonResponse(result)
        except:
            result = {'failed': 'failed'}
            return JsonResponse(result)

    return render(request, 'blog/contact.html', {'title': title})

def add_tag(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    if request.method == 'POST':
        try:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                cd = tag_form.cleaned_data
                post.tags.add(cd['tagname'].lower())
                result = 'success'
                data = {'success': result}
        except:
            result = 'failed'
            data = {'failed': result}
    return JsonResponse(data)

def add_comment(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    parent_obj = None
    result = {}
    parent_id = None

    try:
        if request.method == 'POST':
            # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Here post is the post selected from database by first line of this function

                # Then we check if this is a reply to a comment or a new comment of post
                try:
                    parent_id = int(request.POST.get("parent_id"))
                except:
                    parent_id = None

                if parent_id:
                    parent_qs = Comment.objects.filter(id=parent_id)
                    if parent_qs.exists():
                        parent_obj = parent_qs.first()
                    new_comment.parent = parent_obj
                    # Save the comment to the database
                    new_comment.save()
                    # Send an email to the original commenter
                    cd = comment_form.cleaned_data

                    # Find the parent comment is on which page
                    list_comments = post.comments.filter(active=True, parent=None).order_by('-created')
                    i = 0
                    while(list_comments[i] != parent_obj):
                        i += 1
                    page = i//comment_paginator + 1
                    url = "http://www.minalinsky.info" + post.get_absolute_url() + str(page) + '/'
                    subject = 'Minalinsky Blog Comment System'
                    message = 'Hi, {} replied your comment! Have a check at: \n {}'.format(cd['name'], url)
                    try:
                        send_mail(subject, message, 'jerry574638690@gmail.com', [parent_obj.email])
                    except:
                        print('send email error when reply', parent_obj.email, type(parent_obj.email))
                    # Render the template
                    text = render_to_string('blog/replyhtml.html', {"id": parent_id, "loop": len(parent_obj.children()), "comment": new_comment})
                    result = {"success": text, "max": len(parent_obj.children())}
                else:
                    new_comment.parent = parent_obj
                    # Save the comment to the database
                    new_comment.save()

                    list_comments = post.comments.filter(active=True, parent=None).order_by('-created')
                    paginator = Paginator(list_comments, comment_paginator)

                    comments = paginator.page(1)

                    text = render_to_string('blog/comment_page.html', {"post": post, "comments": comments})
                    result = {"success": text}
    except:
        result = {"failed": "failed"}

    return JsonResponse(result)

def author(request):
    title = 'About author'
    return render(request, 'blog/author.html', {'title': title})

def subscribe(request):
    title = 'Subscribe'

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subscribe = Subscriber(name=name, email=email)
            subscribe.save()
            text = 'success'
            result = {"success": text}
        except:
            text = 'failed'
            result = {"failed": text}
        return JsonResponse(result)

    return render(request, 'blog/subscribe.html', {'title': title})

def custom_page_not_found(request, exception):
    return render(request, 'blog/404.html')

def custom_error(request, exception):
    return render(request, 'blog/500.html')