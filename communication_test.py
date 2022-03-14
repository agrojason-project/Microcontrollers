import serial 
import csv
import requests
from time import time
from requests.exceptions import HTTPError
from models.sensor_data import SensorData
from auth.bearer import AuthBearer
from utils.date import *


BASE_URL = "https://agrojason.herokuapp.com/api"
USER_TOKEN = None
USER_EMAIL = "a@a.com"
USER_PASSWORD = "1234"
DATA = "2"


############################    MAIN    ############################################
def main():
    # set up the serial line
    ser = serial.Serial('/dev/ttyACM0', 9600) # the first argument is the port name  (ex: COM3). Please check the port name in the device manager
    print(read_serial(ser))
    #initialize the date
    date = DateTime()
    # set up the csv file
    file_name = "results.csv"
    with open(file_name, mode='a', newline='') as results_file:
            fieldnames = ['Date - Time','Temperature In','Temperature Out', 'Humidity In','Humidity_out','Light','Soil Moisture','Ph']
            writer = csv.DictWriter(results_file, fieldnames=fieldnames)
            writer.writeheader()
    #make the do while loop
    old_time = 0
    while True:
        # Time 
        tm = time()
        if (tm - old_time > 3600) and (old_time != 0): #for the last Sunday the March
            old_time = tm #GET THE TIME  
        elif old_time - tm> 3300:  #for the last Sunday the October
            old_time = tm #GET THE TIME 
        elif tm - old_time > 29: #299:                    
            old_time = tm #GET THE TIME            
            sensor(ser,file_name,fieldnames,date)   
        #continue 
    ser.close() 


##########################    FUNCTION    ##########################################


def read_serial(ser):  #read a string from the serial line
    b = ser.readline()          # read a byte string
    string_n = b.decode()       # decode byte string into Unicode
    return string_n.rstrip()    # remove \n and \r


def sensor(ser,file_name,fieldnames,date):
    
    ser.write(DATA.encode())
    timestamp = date.get_utc_now()
    temperature_in = float(read_serial(ser))
    temperature_out = float(read_serial(ser))
    humidity_in = float(read_serial(ser))
    humidity_out = float(read_serial(ser))
    light = float(read_serial(ser))
    pH = float(read_serial(ser))
    humidity_substrate = float(read_serial(ser))
    
    
    #send the data in the web app
    data = SensorData(timestamp, temperature_in, temperature_out, humidity_in, humidity_out, light, pH, humidity_substrate) 
    send_data(data)
    #open file to write
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


def send_data(sensorData : SensorData):
    res = send_sensor_data(sensorData)
    if (res is not None): return
    login(USER_EMAIL, USER_PASSWORD)
    if (USER_TOKEN is None):
        return
    send_sensor_data(sensorData)


def login(email: str, password: str):
    try:
        res = requests.post(f"{BASE_URL}/users/login", data = {"email": email, "password": password})
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
        res = requests.post(f"{BASE_URL}/sensors", data = vars(sensorData), auth=AuthBearer(USER_TOKEN))
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