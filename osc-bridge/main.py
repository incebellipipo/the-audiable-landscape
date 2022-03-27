## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#####################################################
## librealsense tutorial #1 - Accessing depth data ##
#####################################################

# First import the library
import pyrealsense2 as rs
import numpy as np
from pythonosc import dispatcher, osc_server, udp_client
from pythonosc.udp_client import SimpleUDPClient
import threading
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.midi
import time
import statistics

RES_WIDTH=848
RES_HEIGHT=480
N_BINS = 8
MAX_RANGE = 0.686 # In meters
MIN_RANGE = 0.35 # In meters
VERTICAL_STEP_SIZE = 10

class Sandbox:
    def __init__(self):
        self._osc_clients = [
            udp_client.SimpleUDPClient("127.0.0.1", 7400),
            udp_client.SimpleUDPClient("127.0.0.1", 7401)
        ]

        self._vertical_position = RES_HEIGHT / 2
        self._vertical_position_operator = VERTICAL_STEP_SIZE # 1 going up, -1 going down

        self._depth = None

        self._button_triggered = False

    def _camera_loop(self):
        print("camera loop starts!")
        try:
            # Create a context object. This object owns the handles to all connected realsense devices
            pipeline = rs.pipeline()

            # Configure streams
            config = rs.config()
            config.enable_stream(rs.stream.depth, RES_WIDTH, RES_HEIGHT, rs.format.z16, 30)

            # Start streaming
            pipeline.start(config)

            while True:
                # This call waits until a new coherent set of frames is available on a device
                # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
                frames = pipeline.wait_for_frames()
                depth = frames.get_depth_frame()
                if not depth: 
                    continue

                depths = []
                thresholded_depths = []
                for x in range(RES_WIDTH):
                    d = statistics.median([
                        depth.get_distance(x, int(RES_HEIGHT / 2.0) - 1),
                        depth.get_distance(x, int(RES_HEIGHT / 2.0)),
                        depth.get_distance(x, int(RES_HEIGHT / 2.0) + 1)
                    ])

                    depths.append(d)
                    if d > MAX_RANGE:
                        thresholded_depths.append(MAX_RANGE)
                    elif d < MIN_RANGE:
                        thresholded_depths.append(MIN_RANGE)
                    else:
                        thresholded_depths.append(d)

                bins = []
                for b in range(N_BINS):
                    idx = int((RES_WIDTH / N_BINS) * b + (RES_WIDTH / N_BINS) / 2)
                    bins.append(thresholded_depths[idx])

                for i in self._osc_clients:
                    i.send_message('/depths', depths)
                    i.send_message('/thresholded_depths', depths)
                    i.send_message('/bins', bins)


                if self._vertical_position >= RES_HEIGHT - abs(VERTICAL_STEP_SIZE):
                    self._vertical_position_operator = -1 * abs(VERTICAL_STEP_SIZE) 
                elif self._vertical_position <= abs(VERTICAL_STEP_SIZE):
                    self._vertical_position_operator = 1 * abs(VERTICAL_STEP_SIZE) 
                self._vertical_position += self._vertical_position_operator

                vertical_depths = [self._vertical_position]
                for x in range(RES_WIDTH):
                    d = depth.get_distance(x, int(self._vertical_position))
                    vertical_depths.append(d)

                for i in self._osc_clients:
                    i.send_message('/vertical_depths', vertical_depths)
                


        except Exception as e:
            print(e)
            pass

    def _button_loop(self):
        print("button loop starts!")
        pygame.init()
        pygame.midi.init()

        l = None 
        for d in range(pygame.midi.get_count()):
            (interf, name, input, output, opened) = pygame.midi.get_device_info(d)
            if input == 1 and "Button" in name.decode():
                l = (d, interf, name, input, output, opened)
                break

        if l is None:
            print("no device can be found!")
            return

        midi_input = pygame.midi.Input(l[0])
        
        try: 
            while True:
                if midi_input.poll():
                    event = midi_input.read(num_events=256)[0]
                    data = event[0]
                    timestamp = event[1]
                    note_number = data[1]
                    velocity = data[2]
                    if note_number == 64 and velocity > 0:
                        self._button_triggered = True
                        for i in self._osc_clients:
                            i.send_message('/button', True)

                time.sleep(0.01)

        except KeyboardInterrupt as err:
            print("Stopping...")

    def run(self):
        camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
        button_thread = threading.Thread(target=self._button_loop, daemon=True)

        camera_thread.start()
        button_thread.start()



def main():
    s = Sandbox()
    s.run()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
