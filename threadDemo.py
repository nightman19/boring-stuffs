import threading, time
print('The Program Just Started!')

def takeANap():
    time.sleep(5)
    print('Wake Up!')


threadObj = threading.Thread(target=takeANap)
threadObj.start()

print('End of Program')