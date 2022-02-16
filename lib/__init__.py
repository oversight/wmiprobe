import asyncio
import logging
import platform
import socket
import os
import sys
import time
import uuid
from aiowmi.connection import Connection
from aiowmi.exceptions import WbemExInvalidClass
from aiowmi.exceptions import WbemExInvalidNamespace
from .check import CHECKS
from .credentials import CREDENTIALS, load_credentials
from .version import __version__


SYSTEM_ID = str(uuid.uuid1()).split('-')[-1]


class Probe:
    probe_name = 'wmiProbe'
    agentcore = None
    credentials_loaded = False
    max_runtime_factor = .8

    @classmethod
    def on_connection_made(cls, protocol):
        cls.agentcore = protocol
        cls.agentcore.send({
            'type': 'probeAnnouncement',
            'hostInfo': cls._get_hostinfo(),
            'platform': cls._get_platform_str(),
            'versionNr': __version__,
            'probeName': cls.probe_name,
            'probeProperties': ['remoteProbe'],
            'availableChecks': {
                k: {
                    'defaultCheckInterval': v.interval,
                    'requiredServices': v.required_services,
                } for k, v in CHECKS.items()
            },
        })

    @classmethod
    def on_connection_lost(cls, protocol):
        cls.agentcore = None

    @staticmethod
    def _get_hostinfo():
        return {
            'timestamp': int(time.time()),
            'hostName': socket.getfqdn(),
            'osFamily': os.name,
            'platform': platform.system(),
            'ip4': socket.gethostbyname(socket.gethostname()),
            'release': platform.release(),
            'systemId': SYSTEM_ID,
            'processStartTs': int(time.time())
        }

    @staticmethod
    def _get_platform_str():
        platform_bits = 'x64' if sys.maxsize > 2 ** 32 else 'x32'
        return f'{platform.system()}_{platform_bits}_{platform.release()}'

    @classmethod
    def on_customer_uuid(cls, data):
        if cls.credentials_loaded:
            return

        # setting this bool will make sure credentails are loaded only once
        cls.credentials_loaded = True

        customer_uuid = data['customerUuid']
        agentcore_uuid = f'{customer_uuid}-{SYSTEM_ID}'
        load_credentials(agentcore_uuid)

    @classmethod
    async def on_run_check(cls, data):
        try:
            host_uuid = data['hostUuid']
            check_name = data['checkName']
            config = data['hostConfig']['probeConfig'][cls.probe_name]
            ip4 = config['ip4']
            interval = data.get('checkConfig', {}).get('metaConfig', {}).get(
                'checkInterval')
            assert interval is None or isinstance(interval, int)
            assert check_name in CHECKS
        except Exception:
            logging.error('invalid check configuration')
            return

        cred = CREDENTIALS.get(ip4, CREDENTIALS.get('defaultCredentials'))
        if cred is None:
            logging.warning(f'missing credentials for {ip4}')
            return

        check = CHECKS[check_name]
        max_runtime = cls.max_runtime_factor * (interval or check.interval)

        try:
            conn = Connection(ip4, **cred)
            await conn.connect()
        except Exception:
            logging.error(f'unable to connect to {host_uuid} {ip4}')
            return

        try:
            service = await conn.negotiate_ntlm()
        except Exception:
            logging.error(f'unable to autheticate {host_uuid} {ip4}')

            conn.close()
            return

        t0 = time.time()
        try:
            state_data = await asyncio.wait_for(
                check.get_data(conn, service),
                timeout=max_runtime
            )
        except asyncio.TimeoutError:
            e = 'check timeout'
            logging.warning(f'on_run_check {host_uuid} {check_name} {e}')
            framework = {'timestamp': t0, 'runtime': time.time() - t0}
            message = 'Check timed out.'

            # ignore when no longer connected
            if cls.agentcore:
                cls.agentcore.send({
                    'type': 'checkError',
                    'hostUuid': host_uuid,
                    'checkName': check_name,
                    'message': message,
                    'framework': framework,
                })
        except (WbemExInvalidClass, WbemExInvalidNamespace):
            # ignore invalid class and namespace errors
            # for citrix, exchange and nvidia checks
            pass
        except Exception as e:
            logging.warning(f'on_run_check {host_uuid} {check_name} {e}')
            framework = {'timestamp': t0, 'runtime': time.time() - t0}
            message = f'Check error: {e.__class__.__name__}: {e}'

            # ignore when no longer connected
            if cls.agentcore:
                cls.agentcore.send({
                    'type': 'checkError',
                    'hostUuid': host_uuid,
                    'checkName': check_name,
                    'message': message,
                    'framework': framework,
                })
        else:
            logging.debug(f'on_run_check {host_uuid} {check_name} ok!')
            framework = {'timestamp': t0, 'runtime': time.time() - t0}

            if cls.agentcore:
                cls.agentcore.send({
                    'type': 'stateData',
                    'hostUuid': host_uuid,
                    'framework': framework,
                    'checkName': check_name,
                    'stateData': state_data
                })
        finally:
            service.close()
            conn.close()
