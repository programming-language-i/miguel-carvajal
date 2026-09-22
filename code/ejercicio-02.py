import threading
import time

TEMPERATURAS = [20, 30, 40, 50, 60]

def sensor(id_sensor, temperatura):
    for lectura in range(5):
        print(f"Sensor {id_sensor} | lectura {lectura}: {temperatura} °C")
        time.sleep(1)

def main():
    for i, temp in enumerate(TEMPERATURAS, start=1):
        hilo = threading.Thread(target=sensor, args=(i, temp))
        hilo.start()
        hilo.join()

    print("Finalizo")

if __name__ == "__main__":
    main()