#kodi

# enable debug logging:  http://kodi.wiki/view/Log_file/Advanced#Enable_debugging
# tail -f /home/osmc/.kodi/temp/kodi.log
# can paste logs at http://xbmclogs.com/

# from http://kodi.wiki/view/Service_addons

# kodi-send --action="XBMC.RunAddon(service.control_red)"

import time
import xbmc
import thread
from lib import websocket

def on_message(ws, message):
	xbmc.executebuiltin("Notification('Message Received','" + message + "',5000)")
	xbmc.log("ws_recv:%s" % message, level=xbmc.LOGDEBUG)

def on_error(ws,error):
	xbmc.log("ws_error:%s" % error)

def on_close(ws):
	xbmc.log("ws_closed", level=xbmc.LOGDEBUG)
 
def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(7)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        xbmc.log("thread terminating...", level=xbmc.LOGDEBUG)
    xbmc.log("thread starting...", level=xbmc.LOGDEBUG)
    thread.start_new_thread(run, ())


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://alexa.hiller.pro:8080/echo",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

 
    while True:
        # Sleep/wait for abort for 10 seconds
        #GOING TO NEED TO ENSURE I CHECK FOR ABORT OF XBMC
        if monitor.waitForAbort(600):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("hello addon! %s" % time.time(), level=xbmc.LOGDEBUG)