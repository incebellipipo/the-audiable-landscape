from pythonosc.dispatcher import Dispatcher
from typing import List, Any
from pythonosc.osc_server import BlockingOSCUDPServer

dispatcher = Dispatcher()

def depth_handle(address, *args):
    print(f"{address}: {args}")

dispatcher.map("/depths", depth_handle)  # Map wildcard address to set_filter function

server = BlockingOSCUDPServer(("127.0.0.1", 7400), dispatcher)
server.serve_forever()