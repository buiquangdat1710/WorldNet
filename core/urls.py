from django.urls import path
from core.views import index
from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name = "feed"),
    path('search/', views.search_view, name='search'),
    path('search/messages/', views.search_messages, name='search_messages'),
    path("post/<slug:slug>/", views.post_detail, name = "post-detail"),
    # Ajax URLS
    path("create_post/", views.create_post, name = "create_post"),
    path("like-post/", views.like_post, name = "like-post"),
    path("comment-post/", views.comment_on_post, name="comment-post"),
    path("like-comment/", views.like_comment, name="like-comment"),
    path("reply-comment/", views.reply_comment, name="reply-comment"),
    path("delete-comment/", views.delete_comment, name="delete-comment"),
    path('delete-post/', views.delete_post, name='delete-post'),
    path("add-friend/", views.add_friend, name="add-friend"),
    path("accept-friend-request/", views.accept_friend_request, name="accept-friend-request"),
    path("reject-friend-request/", views.reject_friend_request, name="reject-friend-request"),
    path("unfriend/", views.unfriend, name="unfriend"),
    path("core/inbox/", views.inbox, name="inbox"),
    path("core/inbox/<username>/", views.inbox_detail, name="inbox_detail"),
    path("block-user/", views.block_user, name="block-user"),
    path('generate-ai-image/', views.generate_ai_image, name='generate_ai_image'),
    path('send-message/', views.send_message, name='send_message'),
    path('translate-prompt/', views.translate_prompt, name='translate_prompt'),
]
