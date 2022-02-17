import argparse
import asyncio
from agentcoreclient import AgentCoreClient
from setproctitle import setproctitle
from lib.check import CHECKS
from lib.credentials import read_credentials
from lib.version import __version__


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

    loop = asyncio.get_event_loop()

    cl = AgentCoreClient(
        'wmiProbe',
        __version__,
        CHECKS,
        read_credentials,
        'wmiProbe-config.json'
    )

    cl.setup_logger(args)

    loop.run_until_complete(
        cl.connect()
    )
    loop.run_until_complete(
        cl.announce()
    )

    loop.run_forever()
