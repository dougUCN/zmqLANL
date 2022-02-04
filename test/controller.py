import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import zmqLanl

'''Basic Local test case'''
router_dealer_addr = 'tcp://127.0.0.1:5560'
status_queue_addr = 'tcp://127.0.0.1:5559'

controller = zmqLanl.Controller(in_socket=status_queue_addr, out_socket=router_dealer_addr)
print('Waiting for workerStatus monitor to launch...')
time.sleep(1)

workerNames = [b'A', b'B', b'C']

print('Greeting workers ', workerNames)
for w in workerNames:
    controller.sendCmd( w, [b'Hello'])

time.sleep(1)
print('Checking for responses...')
print( controller.clearQueue() )
controller.closeQueue()