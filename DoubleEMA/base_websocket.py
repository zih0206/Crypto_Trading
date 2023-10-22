
"""
    Websocket

    1. Log into websocket, and then describe the data...

"""

import json
import sys
import traceback
import socket
from datetime import datetime
from time import sleep
from threading import Lock, Thread
import websocket
import zlib
import time
import hashlib
import hmac
import base64

class Tick(object):
    def __init__(self):
        self.bid_price_1 = 0
        self.bid_price_2 = 0
        self.bid_price_3 = 0
        self.bid_price_4 = 0
        self.bid_price_5 = 0

        self.ask_price_1 = 0
        self.ask_price_2 = 0
        self.ask_price_3 = 0
        self.ask_price_4 = 0
        self.ask_price_5 = 0

        self.bid_volume_1 = 0
        self.bid_volume_2 = 0
        self.bid_volume_3 = 0
        self.bid_volume_4 = 0
        self.bid_volume_5 = 0

        self.ask_volume_1 = 0
        self.ask_volume_2 = 0
        self.ask_volume_3 = 0
        self.ask_volume_4 = 0
        self.ask_volume_5 = 0

class BaseWebsocket(object):
    """         
        Basic Idea:
    1. Needs: Using Start to active worker thread and ping thread after creating Websocket client object
    2. Worker can reconnect the server automatically
    3. Stop: it can stop and ruin web server
    4. we still consider: 
    on open
    on close 
    on msg
    on error
    
    Once the start() was used, ping thread will be active repeatedly per 60s.

    """

    def __init__(self, host=None, ping_interval=20):
        """Constructor"""
        self.host = host
        self.ping_interval = ping_interval

        self._ws_lock = Lock()
        self._ws = None
        # Thread 1
        self._worker_thread = None
        # Thread 2
        self._ping_thread = None
        self._active = False  # Switch

        # debug..
        self._last_sent_text = None
        self._last_received_text = None

    def start(self):
        """
        Active client. It will use on_open method if the client was connected successfully
        Only after on_open, we can send message to server
        """

        self._active = True
        self._worker_thread = Thread(target=self._run)
        self._worker_thread.start()

        self._ping_thread = Thread(target=self._run_ping)
        self._ping_thread.start()

    def stop(self):
        """
        Stop the terminal.
        """
        self._active = False
        self._disconnect()

    def join(self):
        """
        Wait till all threads finish.
        This function cannot be called from worker thread or callback function.
        """
        self._ping_thread.join()
        self._worker_thread.join()

    def send_msg(self, msg: dict):
        """
        Send data to server
        """
        text = json.dumps(msg)
        self._record_last_sent_text(text)
        return self._send_text(text)

    def _send_text(self, text: str):
        """
        send text data to server
        """
        ws = self._ws
        if ws:
            ws.send(text, opcode=websocket.ABNF.OPCODE_TEXT)

    def _ensure_connection(self):
        """"""
        triggered = False
        with self._ws_lock:
            if self._ws is None:
                self._ws = websocket.create_connection(self.host)

                triggered = True
        if triggered:
            self.on_open()

    def _disconnect(self):
        """
        method of disconnet
        """
        triggered = False
        with self._ws_lock:
            if self._ws:
                ws: websocket.WebSocket = self._ws
                self._ws = None

                triggered = True
        if triggered:
            ws.close()
            self.on_close()

    def _run(self):
        """
        keep running, we know the method of stop.
        """
        try:
            while self._active:
                try:
                    self._ensure_connection()
                    ws = self._ws
                    if ws:
                        text = ws.recv()

                        # ws object is closed when recv function is blocking
                        if not text:
                            self._disconnect()
                            continue

                        self._record_last_received_text(text)

                        self.on_msg(text)
                # ws is closed before recv function is called
                # For socket.error, see Issue #1608
                except (websocket.WebSocketConnectionClosedException, socket.error):
                    self._disconnect()

                # other internal exception raised in on_msg
                except:  # noqa
                    et, ev, tb = sys.exc_info()
                    self.on_error(et, ev, tb)
                    self._disconnect()  #

        except:  # noqa
            et, ev, tb = sys.exc_info()
            self.on_error(et, ev, tb)

        self._disconnect()

    def _run_ping(self):
        """"""
        while self._active:
            try:
                self._ping()
            except:  # noqa
                et, ev, tb = sys.exc_info()
                self.on_error(et, ev, tb)
                sleep(1)

            for i in range(self.ping_interval):
                if not self._active:
                    break
                sleep(1)

    def _ping(self):
        """"""
        ws = self._ws
        if ws:
            ws.send("ping", websocket.ABNF.OPCODE_PING)

    def on_open(self):
        """on open """

    def on_close(self):
        """
        on close websocket
        """

    def on_msg(self, data: str):
        """call when the msg arrive."""

    def on_error(self, exception_type: type, exception_value: Exception, tb):
        """
        Callback when exception raised.
        """
        sys.stderr.write(
            self.exception_detail(exception_type, exception_value, tb)
        )

        return sys.excepthook(exception_type, exception_value, tb)

    def exception_detail(
            self, exception_type: type, exception_value: Exception, tb
    ):
        """
        Print detailed exception information.
        """
        text = "[{}]: Unhandled WebSocket Error:{}\n".format(
            datetime.now().isoformat(), exception_type
        )
        text += "LastSentText:\n{}\n".format(self._last_sent_text)
        text += "LastReceivedText:\n{}\n".format(self._last_received_text)
        text += "Exception trace: \n"
        text += "".join(
            traceback.format_exception(exception_type, exception_value, tb)
        )
        return text



    # For debug
    def _record_last_sent_text(self, text: str):
        """
        Record last sent text for debug purpose.
        """
        self._last_sent_text = text[:1000]

    def _record_last_received_text(self, text: str):
        """
        Record last received text for debug purpose.
        """
        self._last_received_text = text[:1000]
