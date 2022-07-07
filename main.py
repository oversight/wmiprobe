import asyncio
from libprobe.probe import Probe
from lib.check.disk_io import check_disk_io
from lib.check.cpu import check_cpu
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'disk_io': check_disk_io,
        'cpu': check_cpu,
    }

    probe = Probe("wmi", version, checks)

    asyncio.run(probe.start())
