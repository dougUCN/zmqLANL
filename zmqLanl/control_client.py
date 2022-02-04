#!/usr/bin/env python
import zmq
from multiprocessing import Process, Queue
from .common import get_list
import time


def workerStatus(out_q, queue_socket, context=None):
    '''Listens to Queue socket and puts messages into out_q'''
    context = context or zmq.Context.instance()
    socket = context.socket(zmq.PULL)
    socket.bind(queue_socket)

    while True:
        out_q.put(socket.recv_multipart())


class Controller:
    '''Zmq client that sends commands to various workers'''
    
    def __init__(self, in_socket, out_socket):
        '''in_socket is an address where the controller expects to receive messages
        out_socket is an address where the controller expects to send messages
        Note: these should be flipped from the Worker sockets
        '''
        
        self.context = zmq.Context.instance()
        self.client = self.context.socket(zmq.ROUTER)
        self.client.setsockopt(zmq.LINGER,0)  # Don't linger on send()
        self.client.bind(out_socket)

        # Launch parallel worker status monitor
        self.q = Queue()
        self.monitor = Process(target=workerStatus, args=(self.q, in_socket,))
        self.monitor.start()
    
    def sendCmd(self, worker_id, cmd):
        '''Sends bytestring cmd to worker_id'''
        toSend = [worker_id]
        toSend.extend( get_list(cmd) ) 
        self.client.send_multipart( toSend )

    def checkQueue(self):
        '''Retrieves one message from the status queue'''
        return self.q.get()

    def clearQueue(self):
        '''Returns all messages that are stored in status queue as a list of lists'''
        messages = []
        while not self.q.empty():
            messages.append( self.checkQueue() )
        return messages

    def closeQueue(self):
        '''Terminates Queue Thread'''
        self.monitor.terminate()
