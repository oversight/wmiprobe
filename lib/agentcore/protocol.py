import asyncio
import json
import logging
from .. import Probe


class Protocol(asyncio.Protocol):

    PROTO_MAP = {
        'echoRequest': lambda protocol, data:
            protocol.send({'type': 'echoResponse'}),
        'echoResponse': lambda protocol, data: None,
        'customerUuid': lambda protocol, data: Probe.on_customer_uuid(data),
        'runCheck': lambda protocol, data:
            asyncio.ensure_future(Probe.on_run_check(data))
    }

    def __init__(self, on_connection_made, on_connection_lost):
        self._on_connection_made = on_connection_made
        self._on_connection_lost = on_connection_lost
        self.transport = None
        self.buffer = None

    def connection_made(self, transport):
        self.transport = transport
        self._on_connection_made()
        Probe.on_connection_made(self)

    def connection_lost(self, reason):
        self._on_connection_lost()
        Probe.on_connection_lost(self)

    def data_received(self, data):
        both = self.buffer + data if self.buffer else data
        if b'\r\n' not in data:
            self.buffer = both
            return
        msgs = both.split(b'\r\n')
        last = msgs.pop()
        self.buffer = last if last else None
        for msg in msgs:
            if not msg:
                continue
            loaded = json.loads(msg, encoding='utf-8')
            tp = loaded.get('type')
            if tp is None:
                logging.warning('invalid message')

            elif tp not in self.PROTO_MAP:
                logging.warning(f'unsupported message type: {tp}')

            else:
                self.PROTO_MAP[loaded['type']](self, loaded)

    def send(self, msg):
        self.transport.write(json.dumps(msg).encode() + b'\r\n')
