# coding: utf-8
import time
import can
import klunk
import klunk.can
import klunk.lidar
import klunk.scheduler
import xbox

if __name__ == "__main__":

    print('Bring up CAN0....')
    #os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()
    car = klunk.car.Car(bus)

    xboxJoystick = xbox.Joystick()
    canThread = klunk.can.Can(bus,car)
    canThread.start()

    car.ready()

    scheduler = klunk.scheduler.Scheduler(car, xboxJoystick)
    scheduler.run()
