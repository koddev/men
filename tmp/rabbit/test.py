# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import pgi

pgi.require_version('Gst', '1.0')
pgi.require_version('GstRtspServer', '1.0')
pgi.require_version('GstVideo', '1.0')
from pgi.repository import GLib, Gst, GstVideo, GstRtspServer

# Gst.init(None)

mainloop = GLib.MainLoop()

adres = '127.0.0.1'
server = GstRtspServer.RTSPServer.new()
server.set_address(adres)
server.set_service('8554')

mounts = server.get_mount_points()

factory = GstRtspServer.RTSPMediaFactory()

factory.set_launch('(device=/dev/video0 ! video/x-raw,width=640,height=480,framerate=30/1 ! queue ! rtph264pay name=pay0 pt=96 )')
# factory.set_launch('(device=/dev/video1 ! video/x-raw,width=640,height=480,framerate=20/1 ! queue ! videoconvert ! x264enc tune=zerolatency ! rtph264pay name=pay0 pt=96 )')
# factory.set_launch('( device=/dev/video1:chroma=mp2v ! ffmpegcolorspace ! video/x-raw,width=1920,framerate=5/1 ! ffmpegcolorspace ! directdrawsink -v )')
#factory.set_launch('(filesrc location=istiklal.mp4 ! qtdemux ! queue ! rtph264pay pt=96 name=pay0 )')
# factory.set_launch('(device=/dev/video1 ! video/x-raw-yuy,width=1280,height=720,framerate=5/1 ! rtph264pay name=pay0 pt=96)')

mounts.add_factory("/test",factory)

server.attach(None)
print('ready:'+ adres)
mainloop.run()