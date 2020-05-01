
# import subprocess
# proc=subprocess.run(['fuser'],stdout=subprocess.PIPE,text=True,input='/dev/video0')

import os



stream = os.popen('fuser /dev/video0')
output=stream.read().strip().split()
for i in output:
    os.kill(int(i),9)
 