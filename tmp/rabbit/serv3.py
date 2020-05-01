#!/usr/bin/env python
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

class RTSP_Server:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer.new()
        self.address = '192.168.100.2' #my RPi's local IP
        self.port = '8554'
        self.launch_description = '(filesrc location=/mnt/sd/istiklal.mp4 ! decodebin ! x264enc ! rtph264pay name=pay0 pt=96)'
        self.server.set_address(self.address)
        self.server.set_service(self.port)
        self.factory = GstRtspServer.RTSPMediaFactory()
        self.factory.set_launch(self.launch_description)
        self.factory.set_shared(True)
        self.mount_points = self.server.get_mount_points()
        self.mount_points.add_factory('/test', self.factory)

        self.server.attach(None)
        print('Stream ready')
        GLib.MainLoop().run()

server = RTSP_Server()
