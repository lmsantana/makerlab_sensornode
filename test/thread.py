import thread

def foo1 ():
    while True:
        print "1"

def foo2():
    while True:
        print "2"

thread.start_new_thread(foo1, ())
thread.start_new_thread(foo2, ())
