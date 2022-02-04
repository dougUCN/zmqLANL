#!/usr/bin/env python
import sys,zmq
from .common import get_list

class Worker:
    '''ZMQ server that waits for commands from Controller and sends responses to Controller
    '''
    def __init__(self, worker_id, in_socket, out_socket):
        '''worker_id is a bytestring that acts as the worker server name
        in_socket is an address where the worker expects to receive messages
        out_socket is an address where the worker expects to send messages
        '''
        self.my_id = worker_id
        self.context = zmq.Context.instance()
        self.worker_in = self.context.socket(zmq.DEALER)
        self.worker_in.setsockopt(zmq.IDENTITY, self.my_id)
        self.worker_in.connect(in_socket)
   
        self.worker_out = self.context.socket(zmq.PUSH)
        self.worker_out.setsockopt(zmq.LINGER,0)  # Don't linger on send()
        self.worker_out.connect(out_socket)
    
    def recvMsg(self):
        '''Waits until a multi-part message is received on the in_socket
        returns a byte string message in list form'''
        return self.worker_in.recv_multipart()

    def sendMsg(self, msg):
        '''Sends worker_id + bytestring msg to out_socket
        msg can be either a list or a nonlist'''
        toSend = [self.my_id]
        toSend.extend( get_list(msg) )
        self.worker_out.send_multipart( toSend )
