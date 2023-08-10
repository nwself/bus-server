import json
from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer

from .models import Game, GameState


class GameConsumer(JsonWebsocketConsumer):
    def connect(self):
        print("Let's accept all incoming connections")
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        # self.player_name = self.scope['url_route']['kwargs']['player_name']
        self.room_group_name = 'chat_%s' % self.game_name

        self.game = Game.objects.filter(name=self.game_name).first()
        if self.game is None:
            self.reject()

        print("Add this unknown person to room {}".format(self.room_group_name))
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        print("Send everyone a new state")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'current_state_message',
                'message': None
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content):
        print("Got some action on the ole websocket")
        print(content)

        # event = content['event']

        self.game.handleEvent(content)

        # who knows, tell everyone else
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'current_state_message',
                'message': None
            }
        )

    # Receive message from room group
    def state_message(self, message):
        event = message['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'event': event
        }))

    # Receive message from room group
    def current_state_message(self, message):
        state = self.game.get_current_state()

        # print("Send state to {}".format(self.player_name))
        # Send message to WebSocket
        self.send(text_data=json.dumps(state))
