#!/usr/bin/env python3

import argparse
import asyncio
import os
import sys

from sipyco import common_args
from sipyco.pc_rpc import simple_server_loop

from artiq_highfinesse.driver import ArtiqHighfinesse, ArtiqHighfinesseSim


def create_wlm_data_file(address):
    # Define the content of the wlmData.ini file with parameters
    content = f"""[default]
version = 4         ; IP version
address = {address} ; device IP
port    = 7171      ; Set/Get TCP port number
port2   = 7172      ; Callback port number
offload = 1
loglevel = 5        ; log level
errormode = 9       ; Error signaling
"""

    file_path = os.path.join(os.getcwd(), "wlmData.ini")
    with open(file_path, "w") as file:
        file.write(content)


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device_ip", default=None, help="Device IP.")
    parser.add_argument(
        "--simulation",
        action="store_true",
        help="Put the driver in simulation mode, even if " "--device is used.",
    )
    common_args.simple_network_args(parser, 3284)
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)
    if not args.simulation and args.device_ip is None:
        print(
            "You need to specify either --simulation or -d/--device "
            "argument. Use --help for more information."
        )
        sys.exit(1)
    if args.device_ip:
        create_wlm_data_file(args.device_ip)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if args.simulation:
            dev = ArtiqHighfinesseSim()
        else:
            dev = ArtiqHighfinesse()
        try:
            simple_server_loop(
                {"artiq_highfinesse": dev},
                common_args.bind_address_from_args(args),
                args.port,
                loop=loop,
            )
        except Exception as e:
            print(f"Server loop has failed: {e}")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
