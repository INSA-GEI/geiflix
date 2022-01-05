# coding: utf-8
import time
import can
import klunk as k
import klunk.xboxController as xC
import klunk.can
import klunk.scheduler

if __name__ == "__main__":

    print('Bring up CAN0....')
    #os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()
    car = k.car.Car(bus)

    xboxThread = xC.XboxController(bus,car)
    xboxThread.start()
    webThread = "TBD"
    canThread = klunk.can.Can(bus,car)
    canThread.start()
    jetsonThread = "TBD"

    scheduler = klunk.scheduler.Scheduler(car, xboxThread.joy)
    while True:
        scheduler.Safety()
        time.sleep(0.1)