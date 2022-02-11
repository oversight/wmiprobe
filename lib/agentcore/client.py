import asyncio
import logging
from .protocol import Protocol


class AgentCoreClient:

    def __init__(self, host, port):
        self._loop = asyncio.get_event_loop()
        self.host = host
        self.port = port
        self.connecting = False
        self.connected = False
        self._protocol = None
        self._keepalive = None

    async def _connect(self):
        conn = self._loop.create_connection(
            lambda: Protocol(
                self.on_connection_made,
                self.on_connection_lost
            ),
            self.host,
            self.port
        )

        self.connecting = True
        try:
            _, self._protocol = await asyncio.wait_for(conn, timeout=10)
        except Exception as e:
            logging.error(f'connecting to agentcore failed: {e}')

        self.connecting = False
        if self._keepalive is None or self._keepalive.done():
            self._keepalive = asyncio.ensure_future(self._keepalive_loop())

    async def _keepalive_loop(self):
        step = 30
        while self.connected:
            await asyncio.sleep(step)
            try:
                self._protocol.send({'type': 'echoRequest'})
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(e)
                self.close()
                break

    async def connect_loop(self):
        initial_step = 2
        step = 2
        max_step = 2 ** 7

        while 1:
            if not self.connected and not self.connecting:
                asyncio.ensure_future(self._connect())
                step = min(step * 2, max_step)
            else:
                step = initial_step
            await asyncio.sleep(step)

    def close(self):
        if self._keepalive is not None:
            self._keepalive.cancel()
            self._keepalive = None
        if self._protocol is not None:
            self._protocol.transport.close()
            self._protocol = None

    def on_connection_made(self):
        logging.warn(f'connected to agentcore')
        self.connected = True

    def on_connection_lost(self):
        logging.error(f'connection to agentcore lost')
        self.connected = False
