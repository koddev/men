import gi
gi.require_version('Gst','1.0')
from gi.repository import GObject, Gst, GstVideo, GstRtspServer

Gst.init(None)


mainloop = GObject.MainLoop()

server = GstRtspServer.RTSPServer()

mounts = server.get_mount_points()

factory = GstRtspServer.RTSPMediaFactory()
factory.set_launch('(/dev/video1 is-live=1 format=YUY2 ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay name=pay0 pt=96 )')

mounts.add_factory("/test", factory)

server.attach(None)

print("stream ready at rtsp://127.0.0.1:8554/test")
mainloop.run()
