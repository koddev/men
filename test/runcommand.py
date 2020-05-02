import os


# import subprocess
# proc=subprocess.run(['fuser'],stdout=subprocess.PIPE,text=True,input='/dev/video0')



stream = os.popen('fuser /dev/video1')
output=stream.read().strip().split()
for i in output:
    os.kill(int(i),9)
    print('killde')

    
stream = os.popen('fuser /dev/video0')
output=stream.read().strip().split()
for i in output:
    os.kill(int(i),9)
    print('killde')


    



  
 