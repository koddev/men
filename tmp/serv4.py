#! /usr/bin/python

# pyrtsp - RTSP test server hack
# Copyright (C) 2013  Robert Swain <robert.swain@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version('Gst','1.0')
gi.require_version('GstRtspServer', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GLib, Gst, GstVideo, GstRtspServer

Gst.init(None)

mainloop = GLib.MainLoop()

server = GstRtspServer.RTSPServer.new()
server.set_address('192.168.100.2')
server.set_service('8554')

mounts = server.get_mount_points()

factory = GstRtspServer.RTSPMediaFactory()
#factory.set_launch('( device=/dev/video1 ! video/x-raw,format=YUY2,width=1280,height=720,framerate=5/1 ! videoconvert ! x264enc ! video/x-h264,profile=high ! rtph264pay name=pay0 pt=96 )')
#factory.set_launch('( device=/dev/video1 ! ffmpegcolorspace ! video/x-raw,width=1920,framerate=5/1 ! ffmpegcolorspace ! directdrawsink -v )')
#factory.set_launch('( filesrc location=/mnt/sd/istiklal.mp4 ! qtdemux ! queue ! rtph264pay pt=96 name=pay0 )')
factory.set_launch('(device=/dev/video1 ! video/x-raw-yuy,width=1280,height=720,framerate=5/1 ! videoconvert ! rtph264pay name=pay0 pt=96)')

mounts.add_factory("/test", factory)

server.attach(None)

print("stream ready at rtsp://127.0.0.1:8554/test")
mainloop.run()
