import json
import logging

from channels import Group
from channels.sessions import channel_session
from pods.handlers import PodHandler
from Infrastructure.public import JsonCustomSerializer, APIAuth
# from UI.dashboard import const
from .views import DashboardChart
from channels.generic.websockets import WebsocketDemultiplexer, WebsocketConsumer, WebsocketMultiplexer, JsonWebsocketConsumer

logger = logging.getLogger(__name__)

class Dashboard(JsonWebsocketConsumer):


    http_user = True
    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ('dashboard',)

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({'accept': True })


    def receive(self, content, **kwargs):

        if content['status']:
            chart = DashboardChart()

            result = {'data1': chart.get_top_restart_pod(), 'data2': chart.list_resources()}
            self.group_send(self.connection_groups()[0], result)

        else:
            result = {'status': False }
            self.group_send(self.connection_groups()[0], result)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass
    # @channel_session
    # def connect(message):
    #     message.reply_channel.send({'accept': True})
    #     Group(const.GROUP_NAME).add(message.reply_channel)
    #
    #
    # @channel_session
    # def ws_disconnect(message):
    #     Group(const.GROUP_NAME).discard(message.reply_channel)
    #
    #
    # @channel_session
    # def ws_receive(message):
    #     data = json.loads(message.content['text'])
    #
    #     if data['status']:
    #             chart = DashboardChart()
    #
    #             Group(const.GROUP_NAME).send({"text": json.dumps(
    #                 {'data1': chart.get_top_restart_pod(), 'data2': chart.list_resources()}, cls=JsonCustomSerializer)})

class PodTerminal(WebsocketConsumer):

    http_user = True
    strict_ordering = False

    def connection_groups(self, **kwargs):
        return ['podterminal']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({'accept': True})

    def receive(self, text=None, bytes=None, **kwargs):
        param = json.loads(text)
        podname = param['name']
        instance = PodHandler(APIAuth())
        ret = instance.open_terminal(podname)
        self.send(text=text, bytes=bytes)

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass



