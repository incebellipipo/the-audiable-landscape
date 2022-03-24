from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.osc_server import BlockingOSCUDPServer

dispatcher = Dispatcher()

def input_handle(address, *args):
    print(f"{address}: {args}")

addresses = ['/button', '/bins']

for address in addresses:
    dispatcher.map(address, input_handle)

server = BlockingOSCUDPServer(("127.0.0.1", 7400), dispatcher)
server.serve_forever()