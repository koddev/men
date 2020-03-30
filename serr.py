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
import time
import asyncio

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GLib, Gst, GstVideo, GstRtspServer

mainloop = GLib.MainLoop()
loopAsync = asyncio.get_event_loop()


def startServer():
    Gst.init(None)

    address = '192.168.1.25'
    server = GstRtspServer.RTSPServer.new()
    server.set_address(address)
    server.set_service('8554')

    auth = GstRtspServer.RTSPAuth()
    token = GstRtspServer.RTSPToken()
    token.set_string('media.factory.role', "user")
    basic = GstRtspServer.RTSPAuth.make_basic("user", "pass")
    auth.add_basic(basic, token)
    server.set_auth(auth)

    mounts = server.get_mount_points()

    factory = GstRtspServer.RTSPMediaFactory()
    permissions = GstRtspServer.RTSPPermissions()
    permissions.add_permission_for_role("user", "media.factory.access", True)
    permissions.add_permission_for_role("user", "media.factory.construct", True)
    factory.set_permissions(permissions)

    # factory.set_launch('( device=/dev/video1 ! video/x-raw,format=YUY2,width=1280,height=720,framerate=10/1 ! videoconvert ! x264enc ! video/x-h264,profile=high ! rtph264pay pt=96 name=pay0 )')
    # factory.set_launch('( device=/dev/video1 ! ffmpegcolorspace ! video/x-raw,width=1920,framerate=5/1 ! ffmpegcolorspace ! directdrawsink -v )')
    # factory.set_launch('( filesrc location=istiklal1.mp4 ! qtdemux ! queue ! rtph264pay pt=96 name=pay0 )')
    factory.set_launch(
        '(device=/dev/video0 ! video/x-raw-yuy,width=1280,height=720,framerate=10/1 ! videoconvert ! rtph264pay name=pay0 pt=96)')

    mounts.add_factory("/test", factory)

    server.attach(None)

    print("stream ready at " + address + ":8554/test")

    mainloop.run()


def stopServer():
    time.sleep(10)
    mainloop.stop()
    exit()


def main():
    asyncio.gather(startServer(), stopServer())


if __name__ == "__main__":
    s = time.perf_counter()
    loopAsync.run_until_complete(main())

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    exit()

