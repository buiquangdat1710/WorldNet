
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import ChatMessage
from userauths.models import User


@receiver(post_save, sender=User)
def add_minic_to_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            minic_user = User.objects.get(email='minic@gmail.com')
            # Tạo một tin nhắn chào mừng hoặc chỉ cần tạo một kết nối
            ChatMessage.objects.create(sender=instance, reciever=minic_user, message="Hello Minic!")
        except User.DoesNotExist:
            # Xử lý trường hợp Minic chưa được tạo
            pass