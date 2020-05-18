# -*- coding: utf-8 -*-
from lb.extensions import io


@io.on('connect')
def connect_recv(data=None):
    print(f'\n\nCONN: {data}\n\n')


@io.on('message')
def message_recv(data=None):
    print(f'\n\nMSG: {data}\n\n')
