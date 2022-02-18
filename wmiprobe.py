import argparse
import asyncio
import os
from agentcoreclient import AgentCoreClient
from setproctitle import setproctitle
from lib.check import CHECKS
from lib.config import read_asset_config
from lib.version import __version__


# Migrate the wmic configuration and credentials
def migrate_config_folder():
    if os.path.exists('/data/config/OsWmicProbe'):
        os.rename('/data/config/OsWmicProbe', '/data/config/wmiprobe')
    if os.path.exists('/data/config/wmiprobe/defaultCredentials.ini'):
        os.rename('/data/config/wmiprobe/defaultCredentials.ini',
                  '/data/config/wmiprobe/defaultAssetConfig.ini')


if __name__ == '__main__':
    setproctitle('wmiprobe')

    migrate_config_folder()

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
        read_asset_config,
        '/data/config/wmiprobe/wmiProbe-config.json'
    )

    cl.setup_logger(args)

    loop.run_until_complete(
        cl.connect()
    )
    loop.run_until_complete(
        cl.announce()
    )

    loop.run_forever()
