#!/usr/bin/env python
# -*- coding:utf-8 vi:ts=4:noexpandtab
# Simple RTSP server. Run as-is or with a command-line to replace the default pipeline

import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')


from gi.repository import Gst, GstRtspServer, GObject,GLib

loop = GObject.MainLoop()
GObject.threads_init()
Gst.init(None)

class MyFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self):
		GstRtspServer.RTSPMediaFactory.__init__(self)

	def do_create_element(self, url):
		s_src = "v4l2src ! video/x-raw,rate=5,width=1920,height=1080 ! videoconvert ! video/x-raw,format=YUY2"
		#s_h264 = "videoconvert ! vaapiencode_h264 bitrate=1000"
		#s_src = "device=/dev/video1 ! video/x-raw,rate=5,width=1920,height=1080,format=YUY2"
		s_h264 = ""
		pipeline_str = "( {s_src} ! queue max-size-buffers=1 name=q_enc ! {s_h264} ! rtph264pay name=pay0 pt=96 )".format(**locals())
		if len(sys.argv) > 1:
			pipeline_str = " ".join(sys.argv[1:])
		print(pipeline_str)
		return Gst.parse_launch(pipeline_str)

class GstServer():
	def __init__(self):
		self.server = GstRtspServer.RTSPServer()
		# self.address = '192.168.1.13'  # my RPi's local IP
		self.port = '8554'
		# self.launch_description = '( playbin uri=file:///home/pi/sample_video.mp4 )'
		# self.server.set_address(self.address)
		self.server.set_service(self.port)
		f = MyFactory()
		f.set_shared(True)
		# f.set_launch(self.launch_description)
		m = self.server.get_mount_points()
		m.add_factory("/test", f)
		self.server.attach(None)
		print('Stream ready')

if __name__ == '__main__':
	s = GstServer()
	loop.run()
