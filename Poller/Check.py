class Check:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

def check():
    a = Check(1, 2)
    b = Check(3, 4)
    a.z = 5
    b.z = 6

    print(a.x, a.y, a.z)
    

def setup():
    PER.setPeriod("Per1",  3)
    PER.setPeriod("Per2",  6)
    PER.setPeriod("Per3",  9)
    PER.setPeriod("Per4", 12)
    PER.setPeriod("Per5", 17)
    
import time

def loop():
    cnt = 0
    while (cnt < 200):
        PER.sleep()                                 # sleep as per the calculated polling period
        
        cnt = cnt+1

        str = ""
        for idx in range(5):
            type = "Per%(idx)d" % { 'idx': (idx+1) }
            str = str + (" %(chk)d" % { 'chk': PER.checkName(type) })

        print("%(cnt)3d - %(tim)s - %(str)s" % { 'cnt': cnt, 'tim': time.ctime(), 'str': str })


def main():
    check()
    
    setup()
    print(PER)
    
    loop()


from Periodics import Periodics
PER = Periodics()

if __name__ == "__main__":
    # execute only if run as a script
    main()
