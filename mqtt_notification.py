#!/usr/bin/python

# Quick example, proof of concept for displaying mqtt messages in the windows 10 notification center.
# Based on example from; https://github.com/jithurjacob/Windows-10-Toast-Notifications
# and inspired by https://github.com/jpmens/mqttwarn/pull/160

# Requires a json message formatted like this 
#	{"sub":"subject","txt":"text"}
# to be sent to the topic, however it will fall back to displaying just the message if no json mesage is found.

# can run it in the background if needed, just use pythonw.exe mqtt_notification.py

# by Matthew Bordignon @bordignon on Twitter Dec-2015


import paho.mqtt.client as mqtt #pip install paho-mqtt
import json

from win32api import *
from win32gui import *
import win32con  #requires pywin32, http://sourceforge.net/projects/pywin32/
import sys, os
import struct
import time

# settings begin
broker = "mosquitto.org"
broker_port = 1883
broker_topic = "test/messages"
# settings end

# Class
class WindowsBalloonTip:
    def __init__(self):
        message_map = { win32con.WM_DESTROY: self.OnDestroy,}

        # Register the window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = 'PythonTaskbar'
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)
     
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

    def balloon_tip(self,title, msg):
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(self.classAtom, "Taskbar",style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, self.hinst, None)
        UpdateWindow(hwnd)

        hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        flags =NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (hwnd, 0, flags, win32con.WM_USER+20, hicon, 'Tooltip')
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, 'Balloon Tooltip', msg, 7000, title,NIIF_INFO))
        
        time.sleep(1)   

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	w.balloon_tip('mqtt notification', 'connected to broker')
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(broker_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	
	try:
		#requires a json message to be sent {"sub":"subject","txt":"text"}
		jsonmsg = json.loads(msg.payload)
		w.balloon_tip(jsonmsg['sub'],jsonmsg['txt'] )
	except:
		#fallback to just displaying the text if no JSON message found.
		w.balloon_tip('mqtt notification', str(msg.payload))

w=WindowsBalloonTip()

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
