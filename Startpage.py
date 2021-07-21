#12개 돌리게하기
#한컴터당 4개씩

import os
import _thread
import threading
import time

START_CATENUM = 0
END_CATNUM = START_CATENUM+2


for x in range(START_CATENUM,END_CATNUM):


    thread = threading.Thread
    thread.start_new_thread(os.system("python singlemode.py"), ())

    time.sleep(10)


