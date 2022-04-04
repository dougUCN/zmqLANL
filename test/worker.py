#!/usr/bin/env python
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import zmqLanl

'''Basic local test case'''
router_dealer_addr = 'tcp://127.0.0.1:5560'
status_queue_addr = 'tcp://127.0.0.1:5559'

if len(sys.argv) < 2:
    print('Test usage: python worker_server.py [worker_id]')
    sys.exit()

worker_id = sys.argv[1].encode('utf-8')
worker = zmqLanl.Worker(worker_id=worker_id, 
                        in_socket=router_dealer_addr, out_socket=status_queue_addr)

print(f'Worker {worker_id} waiting for commands')
msg = worker.recvMsg()
print(f'Worker {worker_id} recieved {msg}')
print(f'Worker {worker_id} echoing message')

worker.sendMsg(b'bye')
print(f'Worker {worker_id} exiting')
