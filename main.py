import time
from logwa.progressbar import ProgressBar

p = ProgressBar(100)
p.start()
for i in range(0, 100):
    p.update()
    p.info("okok")
    time.sleep(0.1)
    if i == 50:
        p.interrupt()
        break
