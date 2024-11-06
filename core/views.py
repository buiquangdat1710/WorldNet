import json
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.text import slugify
import requests
from core.models import ChatMessage, Comment, FriendRequest, Post, ReplyComment, Notification
import shortuuid
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Subquery, OuterRef  
from userauths.models import User


# Notifications Keys
noti_new_like = "New Like"
noti_new_follower = "New Follower"
noti_friend_request = "Friend Request"
noti_new_comment = "New Comment"
noti_comment_liked = "Comment Liked"
noti_comment_replied = "Comment Replied"
noti_friend_request_accepted = "Friend Request Accepted"



@login_required
def index(request):
    posts = Post.objects.filter(active = True, visibility = "Everyone").order_by("-id")
    context = {
        'posts': posts
    }

    return render(request, "core/index.html", context)

def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(full_name__icontains=query) if query else []
    results = ''.join([
        f'<li style="display: flex; align-items: center; margin-bottom: 10px;"><a href="{reverse("userauths:profile", args=[user.username])}" style="display: flex; align-items: center; text-decoration: none; color: inherit;"><img src="{user.profile.image.url}" alt="" class="list-avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;"><div class="list-name">{user.profile.user.full_name}</div></a></li>'
        for user in users
    ]) or '<li>No results found</li>'
    return JsonResponse(results, safe=False)


@login_required
def post_detail(request, slug):
    post = Post.objects.get(active=True, visibility="Everyone", slug = slug)
    context = {
        "p":post
    }
    return render(request, "core/post-detail.html", context)


def send_notification(user, sender , post , comment , notification_type ):
    notification = Notification.objects.create(
        user=user, 
        sender=sender, 
        post=post, 
        comment=comment, 
        notification_type=notification_type
    )
    return notification


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')
        generated_image_url = request.POST.get('generated-image-url')

        # Kiểm tra nếu có URL ảnh AI
        if generated_image_url:
            # Lưu ảnh từ URL ảnh AI vào trường image của Post
            image = generated_image_url

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(
                title=title,
                image=image,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + "-" + str(uniqueid.lower())
            )
            post.save()
            Post.objects.filter(title__startswith="Generated Image:").delete()

            profile_image = ""
            if hasattr(request.user, 'profile') and request.user.profile.image:
                profile_image = request.user.profile.image.url

            return JsonResponse({
                'post': {
                    'title': post.title,
                    'image': post.image.url,
                    "username": post.user.username,
                    "profile_image": profile_image,
                    "date": timesince(post.date),
                    "id": post.id,
                }
            })
        elif title and not image:
            post = Post(
                title=title,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + "-" + str(uniqueid.lower())
            )
            post.save()
            Post.objects.filter(title__startswith="Generated Image:").delete()
            profile_image = ""
            if hasattr(request.user, 'profile') and request.user.profile.image:
                profile_image = request.user.profile.image.url
            return JsonResponse({
                'post': {
                    'title': post.title,
                    "username": post.user.username,
                    "profile_image": profile_image,
                    "date": timesince(post.date),
                    "id": post.id,
                }
            })
        elif not title and image:
            post = Post(
                image=image,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + "-" + str(uniqueid.lower())
            )
            post.save()

            profile_image = ""
            if hasattr(request.user, 'profile') and request.user.profile.image:
                profile_image = request.user.profile.image.url

            return JsonResponse({
                'post': {
                    'image': post.image.url,
                    "username": post.user.username,
                    "profile_image": profile_image,
                    "date": timesince(post.date),
                    "id": post.id,
                }
            })

        else:
            return JsonResponse({'error': 'Invalid post data'}, status=400)

    return JsonResponse({"data": "sent"})



from django.http import JsonResponse
from io import BytesIO
from PIL import Image
import requests
import os
from dotenv import load_dotenv

@csrf_exempt
def generate_ai_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)

        # Gọi API Stability AI với multipart/form-data
        host = f"https://api.stability.ai/v2beta/stable-image/generate/core"

        # Nạp biến môi trường từ file .env
        load_dotenv()

        headers = {
            "Authorization": f"Bearer {os.getenv('STABILITY_KEY')}",
            "Accept": "image/*"
        }
        
        # Sử dụng `files` để gửi dữ liệu dưới dạng `multipart/form-data`
        response = requests.post(
            host, 
            headers=headers, 
            files={"none": "", "prompt": (None, prompt)},
        )
        
        if response.ok:
            # Lưu ảnh từ response
            image_content = response.content
            img = Image.open(BytesIO(image_content))
            
            # Tạo tên file duy nhất
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            filename = f"{uniqueid}.jpg"
            img_path = f"media/user_{request.user.id}/{filename}"
            
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            
            # Lưu ảnh
            img.save(img_path)

            # Lưu đối tượng Post trong CSDL
            post = Post(
                user=request.user,
                title=f"Generated Image: {prompt}",
                image=f"user_{request.user.id}/{filename}",
                visibility="everyone",
                slug=slugify(prompt) + "-" + uniqueid
            )
            post.save()

            # Trả về đường dẫn URL đúng cho ảnh
            return JsonResponse({"image_url": post.image.url})
        else:
            print("Stability API Error:", response.text)
            return JsonResponse({"error": "Failed to generate AI image"}, status=500)
        
@csrf_exempt
def like_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    user = request.user
    bool = False
    if user in post.likes.all():
        post.likes.remove(user)
        bool = False
    else:
        post.likes.add(user)
        bool = True
        if post.user != request.user:
            send_notification(post.user, user, post,None,noti_new_like)

    data = {
        'bool': bool,
        'likes': post.likes.all().count()
    }
    return JsonResponse({"data":data})


@csrf_exempt
def comment_on_post(request):


    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post=post,
        comment=comment,
        user=user
    )

    # Notifications system
    if new_comment.user != post.user:
        send_notification(post.user, user, post, new_comment, noti_new_comment)



    data = {
        "bool":True,
        'comment':new_comment.comment,
        "profile_image":new_comment.user.profile.image.url,
        "date":timesince(new_comment.date),
        "comment_id":new_comment.id,
        "post_id":new_comment.post.id,
        "comment_count":comment_count + int(1),
        "username":new_comment.user.username,
    }
    return JsonResponse({"data":data})

@csrf_exempt
def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False
    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True
        if comment.user != user:
            send_notification(comment.user, user, comment.post, comment, noti_comment_liked)
    data = {
        'bool':bool,
        'likes':comment.likes.all().count()
    }
    return JsonResponse({"data":data})

@csrf_exempt
def reply_comment(request):

    id = request.GET['id']
    reply = request.GET['reply']

    comment = Comment.objects.get(id=id)
    user = request.user

    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )

    if comment.user != user:
        send_notification(comment.user, user, comment.post, comment, noti_comment_replied)


    data = {
        "bool":True,
        'reply':new_reply.reply,
        "profile_image":new_reply.user.profile.image.url,
        "date":timesince(new_reply.date),
        "reply_id":new_reply.id,
        "post_id":new_reply.comment.post.id,
        "username":new_reply.user.username,
    }
    return JsonResponse({"data":data})


@csrf_exempt
def delete_comment(request):
    id = request.GET['id']
    
    comment = Comment.objects.get(id=id)
    comment.delete()

    data = {
        "bool":True,
    }
    return JsonResponse({"data":data})

@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def add_friend(request):
    sender = request.user
    receiver_id = request.GET['id'] 
    bool = False

    if sender.id == int(receiver_id):
        return JsonResponse({'error': 'You cannot send a friend request to yourself.'})
    
    receiver = User.objects.get(id=receiver_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({'error': 'Cancelled', 'bool':bool})
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True
        send_notification(receiver, sender, None, None, noti_friend_request)
        return JsonResponse({'success': 'Sent',  'bool':bool})
    

@csrf_exempt
def accept_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()

    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)

    friend_request.delete()

    send_notification(sender, receiver, None, None, noti_friend_request_accepted)

    data = {
        "message":"Accepted",
        "bool":True,
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
def reject_friend_request(request):
    id = request.GET['id'] 

    receiver = request.user
    sender = User.objects.get(id=id)
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
    friend_request.delete()

    data = {
        "message":"Rejected",
        "bool":True,
    }
    return JsonResponse({'data': data})


@csrf_exempt
def unfriend(request):
    sender = request.user
    friend_id = request.GET['id'] 
    bool = False

    if sender.id == int(friend_id):
        return JsonResponse({'error': 'You cannot unfriend yourself, wait a minute how did you even send yourself a friend request?.'})
    
    my_friend = User.objects.get(id=friend_id)
    
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool = True
        return JsonResponse({'success': 'Unfriend Successfull',  'bool':bool})


@login_required
def inbox(request):
    user_id = request.user

    chat_message = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")

    try:
        minic_user = User.objects.get(email='minic@gmail.com')
        if not ChatMessage.objects.filter(sender=minic_user, reciever=user_id):
            ChatMessage.objects.create(sender=minic_user, reciever=user_id, message="Xin chào bạn, mình là Minic, trợ lý ảo của riêng bạn. Bạn có muốn nói chuyện với mình không ?")
    except User.DoesNotExist:
        pass
    
    context = {
        'chat_message': chat_message,
    }
    return render(request, 'chat/inbox.html', context)


@login_required
def inbox_detail(request, username):
    user_id = request.user
    message_list = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")


    
    sender = request.user
    receiver = User.objects.get(username=username)
    receiver_details = User.objects.get(username=username)
    
    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, reciever=receiver) | Q(sender=receiver, reciever=sender)
    ).order_by("date")

    messages_detail.update(is_read=True)
    
    if messages_detail:
        r = messages_detail.first()
        reciever = User.objects.get(username=r.reciever)
    else:
        reciever = User.objects.get(username=username)

    context = {
        'message_detail': messages_detail,
        "reciever":reciever,
        "sender":sender,
        "receiver_details":receiver_details,
        "message_list":message_list,
    }
    return render(request, 'chat/inbox_detail.html', context)


def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = User.objects.get(id=id)

    if user.id == friend.id:
        return JsonResponse({'error': 'You cannot block yourself'})


    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
    else:
        return JsonResponse({'error': 'You cannot block someone that is not your friend'})

    return JsonResponse({'success': 'User Blocked'})


def search_messages(request):
    query = request.GET.get('q', '')
    if query:
        messages = ChatMessage.objects.filter(
            Q(sender__full_name__icontains=query) | 
            Q(reciever__full_name__icontains=query)
        )
        results = [{'full_name': m.sender.full_name, 'message': m.message} for m in messages]
    else:
        results = []
    return JsonResponse(results, safe=False)

from openai import OpenAI
import markdown
from django.utils.safestring import mark_safe
import os
from dotenv import load_dotenv



chat_memory = {}

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            sender = request.user
            receiver_username = request.POST.get('receiver')
            message = request.POST.get('message')
            if not receiver_username:
                return JsonResponse({'error': 'Missing receiver username.'}, status=400)
            receiver = User.objects.get(username=receiver_username)

            # Nếu người nhận là Minic, tạo câu trả lời
            if receiver.username == 'Minic':
                # Lấy lịch sử hội thoại từ bộ nhớ
                history = chat_memory.get(sender.username, [])

                # Thêm tin nhắn mới vào lịch sử
                history.append({"role": "user", "content": message})

                # Tạo client OpenAI
                # Nạp biến môi trường từ file .env
                load_dotenv()

                client = OpenAI(api_key = os.getenv("API_OPENAI_KEY"))
                
                # Tạo câu trả lời từ Minic
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are Minic, a helpful assistant for the social networking website WorldNet. WorldNet is a platform where users can post updates, react, comment, and interact with friends. You can provide information about the website, help with navigating features like posting, commenting, friend requests, and messaging, and answer questions about WorldNet’s policies. When users ask about you, introduce yourself as Minic, the WorldNet chatbot here to make the experience smooth and answer any questions. Always respond in a friendly and concise manner."},
                        *history
                    ]
                )
                reply = completion.choices[0].message.content



                # Thêm câu trả lời của Minic vào lịch sử
                history.append({"role": "assistant", "content": reply})

                # Cập nhật lịch sử hội thoại trong bộ nhớ
                chat_memory[sender.username] = history

            else:
                # Tạo message mới nếu không phải là Minic
                chat_message = ChatMessage.objects.create(
                    sender=sender,
                    reciever=receiver,
                    message=message,
                )
                reply = None

            return JsonResponse({'success': True, 'reply': reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
