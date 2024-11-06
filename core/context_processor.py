
from core.models import FriendRequest, Notification, ChatMessage
from userauths.models import User
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField

def my_context_processor(request):

    try:
        friend_request = FriendRequest.objects.filter(receiver=request.user).order_by('-id')
    except:
        friend_request = None
    
    try:
        notifications = Notification.objects.filter(user=request.user).order_by('-id')
    except:
        notifications = None

    try:
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
        # Đếm số lượng tin nhắn chưa đọc mà người dùng hiện tại là người nhận
        unread_messages_count = ChatMessage.objects.filter(
            reciever=request.user,
            is_read=False
        ).count()
    except:
        chat_message = None
        unread_messages_count = 0


    return {
        "friend_request": friend_request,
        "notifications": notifications,
        "chat_message":chat_message,
        "unread_messages_count": unread_messages_count,
    }



