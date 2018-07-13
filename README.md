# Personal-Blog
A personal blog source code, build in django 2.0.6 and python 3.5, with wampserver's mysql as database backend.

This blog have a system of comments and replies, with auto-mail function which can inform the original comment's user that there is a reply for him by mail.

And there is also a subscribe function. Once there is a new post, the user who subscribed will receive a mail.

And for the management, we use only the superuser of Django. There is a page of login for the administrator. The username and password is the same as superuser of Django. With login, we can delete the comments and replies, edit the posts, add a new post as draft or published.

The backend of this website is Django, with django-ckeditor as the editor of richtext. The front-end is some pages with bootstrap and jquery, which is a template that I bought here: https://themeforest.net/item/berg-multipurpose-one-page-multi-page-template/12060911?s_rank=1 with my own context and pictures.

The third-party library used in this site: django-ckeditor, django-taggit, Markdown. We can install like: pip install django-ckeditor or pip3 install django-taggit according to you use python 2 or 3

Welcome for anyone who has questions of this website to contact me at: jerry574638690@gmail.com
