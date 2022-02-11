import argparse
import asyncio
import os
from setproctitle import setproctitle
from lib.agentcore.client import AgentCoreClient
from lib.config import CONFIG
from lib.logger import setup_logger


AGENTCORE_IP = os.getenv('OS_AGENTCORE_IP', CONFIG.get('agentCoreIp', 'localhost'))
AGENTCORE_PORT = os.getenv('OS_AGENTCORE_PORT', CONFIG.get('agentCorePort', 7211))


if __name__ == '__main__':
    setproctitle('OsWmiProbe.bin')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--log-level',
        default='warning',
        help='set the log level',
        choices=['debug', 'info', 'warning', 'error'])

    parser.add_argument(
        '--log-colorized',
        action='store_true',
        help='use colorized logging')

    args = parser.parse_args()

    setup_logger(args)

    cl = AgentCoreClient(AGENTCORE_IP, AGENTCORE_PORT)

    asyncio.get_event_loop().run_until_complete(
        cl.connect_loop()
    )
