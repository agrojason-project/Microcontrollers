import serial 
from time import  localtime, strftime, sleep
import csv

def read_serial(ser):
    b = ser.readline()         # read a byte string
    string_n = b.decode()      # decode byte string into Unicode
    string = string_n.rstrip() # remove \n and \r
    return float(string)

# set up the serial line
port = "" # path to port
port = port + input("Enter the port: ")
ser = serial.Serial(port, 9600)
print("Set up is OK")
sleep(2)
# set up the csv file
with open('results.csv', mode='a', newline='') as results_file:
        fieldnames = ['Date - Time','Temperature In','Temperature Out', 'Humidity In','Humidity_out','Light','Soil Moisture','Ph']
        writer = csv.DictWriter(results_file, fieldnames=fieldnames)
        writer.writeheader()

# Read and record the data
while True:
    # Time 
    date = strftime("%Y %m %d %H:%M:%S", localtime())
    #Temperature
    Temperature_in = read_serial(ser)
    Temperature_out = read_serial(ser)
    #Humidity
    Humidity_in = read_serial(ser)
    Humidity_out = read_serial(ser)
    #ligth
    light = read_serial(ser)
    #soil moisture
    soil_moisture = read_serial(ser)
    #ph
    ph = read_serial(ser)
    #open file to write
    with open('results.csv', mode='a', newline='') as results_file:
        # csv writer object
        writer = csv.DictWriter(results_file, fieldnames=fieldnames, dialect='excel')
        writer.writerow({'Date - Time':date,'Temperature In':Temperature_in,'Temperature Out':Temperature_out, 'Humidity In':Humidity_in,'Humidity_out':Humidity_out
        ,'Light':light, 'Soil Moisture':soil_moisture, 'Ph':ph})
    sleep(300)
ser.close() 