import threading

import gyue.plugins.Gyue.botFunctions.livePusher as lp
def startThread():
    livestatChk = threading.Thread(target=lp.livecheck)
    livestatChk.start()
    return