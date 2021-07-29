#12개 돌리게하기
#한컴터당 4개씩

import os
import _thread
import threading
import time
import Global

for _ in range (1,20):
    os.system("python multimode-all.py")
    Global.cat3 += 1
    Global.cat4 = 1
    time.sleep(10)