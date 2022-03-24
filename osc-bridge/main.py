## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#####################################################
## librealsense tutorial #1 - Accessing depth data ##
#####################################################

# First import the library
import pyrealsense2 as rs
import numpy as np
from dotenv import dotenv_values 
from pythonosc import dispatcher, osc_server, udp_client
from pythonosc.udp_client import SimpleUDPClient

dotenv_values('.env')

def main():
    client = udp_client.SimpleUDPClient("127.0.0.1", 7400)

    try:
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = rs.pipeline()

        # Configure streams
        config = rs.config()
        config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

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
            for x in range(848):
                depths.append(depth.get_distance(x, 240))

            n_bins = 8
            bins = []
            for b in range(n_bins):
                idx = int((848 / n_bins) * b + (848 / n_bins) / 2)
                bins.append(depths[idx])


            client.send_message('/depths', depths)
            client.send_message('/bins', bins)

        exit(0)
    #except rs.error as e:
    #    # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
    #    print("pylibrs.error was thrown when calling %s(%s):\n", % (e.get_failed_function(), e.get_failed_args()))
    #    print("    %s\n", e.what())
    #    exit(1)
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()