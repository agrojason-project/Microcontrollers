import http.client
import serial 
import csv
from threading import Thread
from datetime import datetime
from pytz import timezone
from time import  sleep, strptime,time

############################    MAIN    ############################################
def main():
    # set up the serial line
    ser = serial.Serial('COM3', 9600) # the first argument is the port name  (ex: COM3). Please check the port name in the device manager
    # set up the csv file
    file_name = "res_th.csv"
    with open(file_name, mode='a', newline='') as results_file:
            fieldnames = ['Date - Time','Temperature In','Temperature Out', 'Humidity In','Humidity_out','Light','Soil Moisture','Ph']
            writer = csv.DictWriter(results_file, fieldnames=fieldnames)
            writer.writeheader()
    #make the do while loop
    x = Thread(target=thread_function, args=(ser,file_name,fieldnames))
    x.start()
    #
    #
    #x.join()    
    #ser.close() 

##########################    FUNCTION    ##########################################

def read_serial(ser):  #read a string from the serial line
    b = ser.readline()          # read a byte string
    string_n = b.decode()       # decode byte string into Unicode
    return string_n.rstrip()    # remove \n and \r  

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

def thread_function(ser,file_name,fieldnames):
    while True:
        # Time          
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
        #data and time
        date = time_request() 
        #open file to write
        with open(file_name, mode='a', newline='') as results_file:
            # csv writer object
            writer = csv.DictWriter(results_file, fieldnames=fieldnames, dialect='excel')
            writer.writerow({'Date - Time':date,'Temperature In':Temperature_in,'Temperature Out':Temperature_out, 'Humidity In':Humidity_in,'Humidity_out':Humidity_out,'Light':light, 'Soil Moisture':soil_moisture, 'Ph':ph})
        sleep(299.35) #sleep for 5 minutes           

######################    START THE PROGRAM    #####################################
if __name__ == '__main__':
    main()