# chat/views.py
import logging
import os
import pprint
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import render


def indexs(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('chat_%s' % room_name, {
        'type': 'chat_message',
        'message': 'triggered'
    })
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

logger = logging.getLogger(__name__)

def room_test(request, room_name, message):

    def cok():
        logger.debug('Coooooook')
        print('Coooooook')
        with open(os.path.join('D:\\data', 'installed.py'), 'w+') as installed:
            info = {
                'application': True,
                'summary': '',
                'description': '',
                'icon': 'icon.ico',
                'author': 'syifarahmat.id',
                'company': 'Karya Waktu Luang',
                'website': 'https://syifarahmat.github.io/',
                'category': 'Uncategorized',
                'version': '1.0',
                'depends': [],
                'runtime': True,
                'installed': datetime.now(),
            }
            printer = pprint.PrettyPrinter(indent=2, stream=installed)
            print('import datetime', file=installed)
            print('', file=installed)
            print('maniferst = \\', file=installed)
            printer.pprint(info)
            installed.close()

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('%s' % room_name, {
        'type': 'chat_message',
        'message': message
    })
    return JsonResponse(dict(ok=True))
