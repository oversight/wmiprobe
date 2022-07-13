import asyncio
from libprobe.probe import Probe
from lib.check.cpu import check_cpu
from lib.check.disk_io import check_disk_io
from lib.check.disk_queue_length import check_disk_queue_length
from lib.check.exchange_queue import check_exchange_queue
from lib.check.cim_datafile import cim_datafile
from lib.check.ica_session import check_ica_session
from lib.check.installed_software import check_installed_software
from lib.check.ip4_route_table import check_ip4_route_table
from lib.check.logged_on_users import check_logged_on_users
from lib.check.memory import check_memory
from lib.check.network_adapter import check_network_adapter
from lib.check.network_interface import check_network_interface
from lib.check.nt_domain import check_nt_domain
from lib.check.nt_eventlog import check_nt_eventlog
from lib.check.nvidia_gpu import check_nvidia_gpu
from lib.check.nvidia_gpu_temperature import check_nvidia_temperature
from lib.check.os_memory import check_os_memory
from lib.check.page_file import check_page_file
from lib.check.pnp_entity import check_pnp_entity
from lib.check.process import check_process
from lib.check.remote_users import check_remote_users
from lib.check.services import check_services
from lib.check.system_time import check_system_time
from lib.check.updates import check_updates
from lib.check.uptime import check_uptime
from lib.check.volume import check_volume
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'cpu': check_cpu,
        'disk_io': check_disk_io,
        'disk_queue_length': check_disk_queue_length,
        'exchange_queue': check_exchange_queue,
        'cim_datafile': check_cim_datafile,
        'ica_session': check_ica_session,
        'installed_software': check_installed_software,
        'ip4_route_table': check_ip4_route_table,
        'logged_on_users': check_logged_on_users,
        'memory': check_memory,
        'network_adapter': check_network_adapter,
        'network_interface': check_network_interface,
        'nt_domain': check_nt_domain,
        'nt_eventlog': check_nt_eventlog,
        'nvidia_gpu_temperature': check_nvidia_temperature,
        'nvidia_gpu': check_nvidia_gpu,
        'os_memory': check_os_memory,
        'page_file': check_page_file,
        'pnp_entity': check_pnp_entity,
        'process': check_process,
        'remote_users': check_remote_users,
        'services': check_services,
        'system_time': check_system_time,
        'updates': check_updates,
        'uptime': check_uptime,
        'volume': check_volume,
    }

    probe = Probe("wmi", version, checks)

    asyncio.run(probe.start())
