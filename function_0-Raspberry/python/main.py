import klunk.car
import klunk.scheduler

if __name__ == "__main__":
    car = klunk.car.Car()
    car.hello_sequence()

    scheduler = klunk.scheduler.Scheduler(car)
    scheduler.run()
