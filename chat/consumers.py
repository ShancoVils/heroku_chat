# Импорт для работы с JSON
import json
from threading import Event 
from asgiref.sync import async_to_sync
# Импорт для асинхронного программирования
from channels.generic.websocket import WebsocketConsumer
# Импорт для работы с БД в асинхронном режиме
from channels.db import database_sync_to_async
# Импорт модели сообщений
from .models import Message
from urllib import parse 
import os
import base64 
from django.core.files.base import ContentFile
import uuid
from django.conf import settings



# Класс ChatConsumer
class ChatConsumer(WebsocketConsumer):
    
    # Метод подключения к WS
    def connect(self):
        # Назначим пользователя в комнату
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        # Добавляем новую комнату
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    # Метод для отключения пользователя
    def disconnect(self, close_code):
        # Отключаем пользователя
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
 
        
 
    # Принимаем сообщение от пользователя
    def receive(self, text_data):
        # Форматируем сообщение из JSON
        text_data_json = json.loads(text_data)
        # Получаем текст сообщения
        name_user = text_data_json['nickname']
        message = text_data_json['message']
        image_data = text_data_json['image_data']

        Message.objects.create(text=message, nickname = name_user)
        
        
        # Отправляем сообщение 
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'nickname': name_user,
                'message': message,
                'image_data': image_data,
            }
        )
        imgData = image_data.split(',', maxsplit=1)[1]# Берем всё что находится после запятой, то есть сам Base64
        ImgGUID = str(uuid.uuid4())#Генерируем гуид для названия картинки
        imgSaveURL = settings.MEDIA_ROOT + '/message_image/' + ImgGUID + '.jpg'# Путь куда сохранять картинку
        with open(imgSaveURL, "wb") as fh:
            fh.write(base64.decodebytes(imgData.encode()))#
        imgSaveURL = imgSaveURL[39:]
    
    # Метод для отправки сообщения клиентам
    def chat_message(self, event):
        # Получаем сообщение от receive
        nickname = event['nickname']
        message = event['message']
        image_data = event['image_data']
        # Отправляем сообщение клиентам
        self.send(text_data=json.dumps({
            'nickname': nickname,
            'message': message,
            'image_data':image_data,
        }, ensure_ascii=False))



