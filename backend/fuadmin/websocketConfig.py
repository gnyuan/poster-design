# -*- coding: utf-8 -*-
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json

from channels.layers import get_channel_layer
from jwt import InvalidSignatureError

from fuadmin.settings import SECRET_KEY


# 发送消息结构体
def set_message(sender, msg_type, msg, refresh_unread=False):
    text = {
        'sender': sender,  # system为系统，其他为客户
        'contentType': msg_type,  # SYSTEM为系统消息
        'content': msg,  # 消息内容
        'refresh_unread': refresh_unread
    }
    return text


# 异步获取消息中心的目标用户
@database_sync_to_async
def _get_message_center_instance(message_id):
    from system.models import MessageCenter
    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list('target_user', flat=True)
    if _MessageCenter:
        return _MessageCenter
    else:
        return []


@database_sync_to_async
def _get_message_unread(user_id):
    """获取用户的未读消息数量"""
    from system.models import MessageCenterTargetUser
    count = MessageCenterTargetUser.objects.filter(users=user_id, is_read=False).count()
    return count or 0

class FuadminWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            import jwt
            print('start socket')
            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            decoded_result = jwt.decode(self.service_uid, SECRET_KEY, algorithms=["HS256"])
            # 本项目而言解码出来的内容有
            #{'exp': 1697045288, 'last_login': None, 'is_superuser': True, 'is_staff': True
            # , 'is_active': True, 'date_joined': '2023-10-09 13:47:23', 'id': 512
            # , 'remark': None, 'creator': None, 'modifier': None, 'belong_dept': None
            # , 'sort': 512, 'username': 'yuangn', 'email': '邮箱'
            # , 'mobile': '电话号码', 'name': '中文全名', 'status': True, 'gender': 1
            # , 'user_type': 0, 'dept': 549, 'first_name': '中文名字', 'last_name': '中文姓氏'
            # , 'groups': [], 'user_permissions': [], 'post': [], 'role': []}
            if decoded_result:
                self.user_id = decoded_result.get('id')
                self.room_name = "user_" + str(self.user_id)
                # 收到连接时候处理，
                await self.channel_layer.group_add(
                    "fuadmin",
                    self.channel_name
                )
                await self.channel_layer.group_add(
                    self.room_name,
                    self.channel_name
                )
                await self.accept()
                # 主动推送消息
                unread_count = await _get_message_unread(self.user_id)
                if unread_count == 0:
                    # 发送连接成功
                    await self.send_json(set_message('system', 'SYSTEM', '连接成功'))
                else:
                    await self.send_json(
                        set_message('system', 'SYSTEM', "请查看您的未读消息~",
                                    refresh_unread=True))
        except InvalidSignatureError:
            await self.disconnect(None)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.channel_layer.group_discard("fuadmin", self.channel_name)
        print("连接关闭")
        try:
            await self.close(close_code)
        except Exception:
            pass


class MegCenter(FuadminWebSocket):
    """
    消息中心
    """

    async def receive(self, text_data):
        # 接受客户端的信息，你处理的函数
        if str(text_data)!='ping':
            text_data_json = json.loads(str(text_data))
            print('receive websocket message: ' + str(text_data_json))
        # message_id = text_data_json.get('message_id', None)
        # user_list = await _get_message_center_instance(message_id)
        # for send_user in user_list:
        #     await self.channel_layer.group_send(
        #         "user_" + str(send_user),
        #         {'type': 'push.message', 'json': text_data_json}
        #     )

    async def push_message(self, event):
        """消息发送"""
        message = event['json']
        print('send websocket message: ' + str(message))
        await self.send(text_data=json.dumps(message))


def websocket_push(room_name, message):
    """
    主动推送
    @param room_name: 群组名称
    @param message: 消息内容
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            "type": "push.message",
            "json": message
        }
    )