from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('author/', views.author, name='author'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('list/', views.post_list, name='post_list_view'),
    path('draft/', views.draft_post_list, name='draft_post_list_view'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('list/<int:page>', views.post_list_page, name='post_list_single_page'),
    path('tag/<slug:tag_slug>/<int:page>', views.post_list_page, name='post_list_by_tag_single_page'),
    path('draft/<int:page>', views.draft_list_page, name='draft_post_list_single_page'),
    path('addpost/', views.add_post, name='add_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail_view'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/<int:page>', views.post_detail, name='post_detail_view_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/edit/', views.edit_post, name='edit_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/editdraft/', views.edit_draft, name='edit_draft'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/share/', views.post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/deletecomment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/addtag/', views.add_tag, name='addtag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/comment/', views.add_comment, name='add_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/comment_page/<int:page>/', views.comment_page, name='comment_single_page'),
]