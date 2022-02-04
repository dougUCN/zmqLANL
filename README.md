zmqLanl
================
This minimal python library provides a ZeroMQ (zmq) wrapper for interface with the LANL nEDM main control system.
The idea of this package is that as the communication network for the LANL control system gets increasingly complicated,
users will not have to learn the details and simply have to run a simple `worker.recvMsg()` or `worker.sendMsg()` to interface with the slow control

Installation
---------------

Dependencies for this package can easily be installed using `pip3 install -r dependencies.txt`

Afterwards, simply copy the directory `zmqLanl` and keep it in the same directory as your python project. You will be able to call the package using `import zmqLanl`

As of 02/03/2022 tested on python version 3.6.9 on Ubuntu 18.04.4 LTS

Example usage
--------------

See `test/worker.py` and `test/controller.py` for an example illustrating communication between a main control system and worker servers.

Run `python worker.py A & python worker.py B & python worker.py C & python controller.py` to view a basic call and response example

Notice how even if you leave out `python worker.py B & python worker.py C` the controller does not hang

Additionally, if you leave out `python controller.py` the workers will wait patiently until the controller is launched


ZeroMQ design layout overview
-------------------------------

For the LANL nEDM control layout, we have multiple *worker* servers (such as the fast daq adc, magnetometer readouts, environmental monitoring, etc).
These workers as designated as zmq *dealers*. These worker servers wait for commands from the the *main control system*, designated as a zmq *router*. It is of
note that the main control system sends commands without waiting for responses to avoid hanging if a worker server is inactive/unresponsive.

The worker servers send outbound status/response messages via zmq *push* to a queue that is hosted on the main control system. The main control system
can then check the queue messages via zmq *pull* at its own leisure.

Command documentation
------------------------

```
class Worker(builtins.object)
 |  ZMQ server that waits for commands from Controller and sends responses to Controller
 |
 |  Methods defined here:
 |
 |  __init__(self, worker_id, in_socket, out_socket)
 |      worker_id is a bytestring that acts as the worker server name
 |      in_socket is an address where the worker expects to receive messages
 |      out_socket is an address where the worker expects to send messages
 |
 |  recvMsg(self)
 |      Waits until a multi-part message is received on the in_socket
 |      returns a byte string message in list form
 |
 |  sendMsg(self, msg)
 |      Sends worker_id + bytestring msg to out_socket
 |      msg can be either a list or a nonlist

class Controller(builtins.object)
 |  Zmq client that sends commands to various workers
 |
 |  Methods defined here:
 |
 |  __init__(self, in_socket, out_socket)
 |      in_socket is an address where the controller expects to receive messages
 |      out_socket is an address where the controller expects to send messages
 |      Note: these should be flipped from the Worker sockets
 |
 |  checkQueue(self)
 |      Retrieves one message from the status queue
 |
 |  clearQueue(self)
 |      Returns all messages that are stored in status queue as a list of lists
 |
 |  closeQueue(self)
 |      Terminates Queue Thread
 |
 |  sendCmd(self, worker_id, cmd)
 |      Sends bytestring cmd to worker_id
```
