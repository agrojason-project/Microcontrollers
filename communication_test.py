import serial
import csv
import requests
import socket

import threading
from time import time
from requests.exceptions import HTTPError
from models.sensor_data import SensorData
from auth.bearer import AuthBearer
from utils.date import *

BASE_URL = "https://agrojason.herokuapp.com/api"
USER_TOKEN = None
USER_EMAIL = "a@a.com"
USER_PASSWORD = "1234"
mutex = threading.Lock()
FAN = "1"
DATA = "2"
IDEAL = "3"

op = None


############################    MAIN    ############################################
def main():
    # set up the serial line
    ser = serial.Serial('/dev/ttyACM0',
                        9600)  # the first argument is the port name  (ex: COM3). Please check the port name in the device manager
    print(read_serial(ser))
    st = threading.Thread(target=read_stdin, args=()).start()
    onl = threading.Thread(target=read_online, args=()).start()
    # initialize the date
    date = DateTime()
    # set up the csv file
    file_name = "results.csv"
    with open(file_name, mode='a', newline='') as results_file:
        fieldnames = ['Date - Time', 'Temperature In', 'Temperature Out', 'Humidity In', 'Humidity_out', 'Light',
                      'Soil Moisture', 'Ph']
        writer = csv.DictWriter(results_file, fieldnames=fieldnames)
        writer.writeheader()
    # make the do while loop
    old_time = 0
    global op
    while True:
        if op != None:
            if op == "exit":
                st.join(2)
                onl.join(2)
                break
            sensor(ser, file_name, fieldnames, date, op)
            op = None
        # Time 
        tm = time()
        if (tm - old_time > 3600) and (old_time != 0):  # for the last Sunday the March
            old_time = tm  # GET THE TIME
        elif old_time - tm > 3300:  # for the last Sunday the October
            old_time = tm  # GET THE TIME
        elif tm - old_time > 299:  # 299:
            old_time = tm  # GET THE TIME
            sensor(ser, file_name, fieldnames, date, DATA)
    ser.close()


##########################    FUNCTION    ##########################################

def read_stdin():
    while True:
        global op
        tmp = input()
        mutex.acquire()
        while op is not None:
            pass
        op = tmp
        while op is not None:
            pass
        mutex.release()


def read_online():
    global op
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind(("", 12345))
    client.listen()
    while True:
        server, addr = client.accept()
        tmp = server.recv(1024)
        mutex.acquire()
        while op is not None:
            pass
        op = tmp.decode()
        while op is not None:
            pass
        server.sendall("OK".encode())
        server.close()
        mutex.release()


def read_serial(ser):  # read a string from the serial line
    b = ser.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    return string_n.rstrip()  # remove \n and \r


def sensor(ser, file_name, fieldnames, date, op):
    ser.write(op[0].encode())
    if op[0] == FAN:
        ser.write(op[1].encode())  # 0:Close, 1:Open
        if read_serial(ser):  # 0:Error, 1:Succeses
            print("FAN Succeses!!")
        else:
            print("FAN Error!!")
    elif op[0] == DATA:
        timestamp = date.get_utc_now()
        temperature_in = float(read_serial(ser))
        temperature_out = float(read_serial(ser))
        humidity_in = float(read_serial(ser))
        humidity_out = float(read_serial(ser))
        light = float(read_serial(ser))
        pH = float(read_serial(ser))
        humidity_substrate = float(read_serial(ser))
        # send the data in the web app
        data = SensorData(timestamp, temperature_in, temperature_out, humidity_in, humidity_out, light, pH,
                          humidity_substrate)
        send_data(data)
        # open file to write
        with open(file_name, mode='a', newline='') as results_file:
            # csv writer object
            writer = csv.DictWriter(results_file, fieldnames=fieldnames, dialect='excel')
            writer.writerow({
                'Date - Time': timestamp,
                'Temperature In': temperature_in,
                'Temperature Out': temperature_out,
                'Humidity In': humidity_in,
                'Humidity_out': humidity_out,
                'Light': light,
                'Soil Moisture': humidity_substrate,
                'Ph': pH
            })
    elif op[0] == IDEAL:
        pass
    else:
        print("## Not good Argument!!!")


def send_data(sensorData: SensorData):
    res = send_sensor_data(sensorData)
    if (res is not None): return
    login(USER_EMAIL, USER_PASSWORD)
    if (USER_TOKEN is None):
        return
    send_sensor_data(sensorData)


def login(email: str, password: str):
    try:
        res = requests.post(f"{BASE_URL}/users/login", data={"email": email, "password": password})
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None
    else:
        global USER_TOKEN
        USER_TOKEN = res.json()['token']


def send_sensor_data(sensorData: SensorData):
    try:
        if (USER_TOKEN is None): return None
        res = requests.post(f"{BASE_URL}/sensors", data=vars(sensorData), auth=AuthBearer(USER_TOKEN))
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None
    else:
        print(res.json())


######################    START THE PROGRAM    #####################################
if __name__ == '__main__':
    main()
