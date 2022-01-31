import http.client
import serial 
import csv
from datetime import datetime
from pytz import timezone
from time import  strptime, time

import requests
from requests.exceptions import HTTPError
from auth.bearer import AuthBearer
from utils.date import DateTime
from models.sensor_data import SensorData

BASE_URL = "https://agrojason.herokuapp.com/api"
USER_TOKEN = None
USER_EMAIL = "a@a.com"
USER_PASSWORD = "1234"


############################    MAIN    ############################################
def main():
    # set up the serial line
    ser = serial.Serial('COM3', 9600) # the first argument is the port name  (ex: COM3). Please check the port name in the device manager
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
        elif tm - old_time > 299:                    
            old_time = tm #GET THE TIME            
            sensor(ser,file_name,fieldnames)
            print("Data sent")            
        #continue 
    ser.close() 

##########################    FUNCTION    ##########################################

def read_serial(ser):  #read a string from the serial line
    b = ser.readline()          # read a byte string
    string_n = b.decode()       # decode byte string into Unicode
    return string_n.rstrip()    # remove \n and \r

def sensor(ser,file_name,fieldnames):
    while read_serial(ser) != "hi": # Wait for the serial line to be ready
        pass  
    #Temperature
    Temperature_in = float(read_serial(ser))
    Temperature_out = float(read_serial(ser))
    #Humidity
    Humidity_in = float(read_serial(ser))
    Humidity_out = float(read_serial(ser))
    #ligth
    light = float(read_serial(ser))
    #soil moisture
    soil_moisture = float(read_serial(ser))
    #ph
    ph = float(read_serial(ser))
    #send the data in the web app
    send_data(Temperature_in,Temperature_out, Humidity_in,Humidity_out,light, soil_moisture, ph)
    #data and time
    date = time_request() 
    #open file to write
    with open(file_name, mode='a', newline='') as results_file:
        # csv writer object
        writer = csv.DictWriter(results_file, fieldnames=fieldnames, dialect='excel')
        writer.writerow({'Date - Time':date,'Temperature In':Temperature_in,'Temperature Out':Temperature_out, 'Humidity In':Humidity_in,'Humidity_out':Humidity_out,'Light':light, 'Soil Moisture':soil_moisture, 'Ph':ph})

def time_request(): #return the date and time in the format of the csv file
    conn = http.client.HTTPConnection('google.com') 
    conn.request("GET", "/")
    r = conn.getresponse()
    r.getheaders() #Get all http headers
    ts = r.getheader('date') # Get the date part of the http header
    ltime = strptime(ts[5:25], "%d %b %Y %H:%M:%S") 
    fmt = "%Y/%m/%d %H:%M:%S"
    now_time = datetime.now(timezone('Europe/Athens')) #get the current time
    return now_time.strftime(fmt) #return the current time in the format of the csv file


def send_data(Temperature_in,Temperature_out, Humidity_in,Humidity_out,light, soil_moisture, ph):
    utc_now = DateTime.get_utc_now()
    sensorData = SensorData(utc_now, Temperature_in,Temperature_out, Humidity_in,Humidity_out,light, soil_moisture, ph)
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