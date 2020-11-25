from threading import Timer

def api_call():
    print("Call that there api")

def newTimer():
    global t
    t = Timer(10.0,api_call)
newTimer()


def my_callback(channel):

    if something_true:
        print('reset timer and start again')
        t.cancel()
        newTimer()
        t.start()
        print("\n timer started")


