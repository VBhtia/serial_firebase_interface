import serial
import time
import requests
import json

#Connection to firebase
firebase_url = '****************'


#Connect to Serial Port for communication
ser = serial.Serial('COM7', 115200, timeout=0)



fixed_interval = 2
while 1:
  try:
    msg = ser.readline() # read all characters in buffer
 
    value= msg.decode('ascii').strip().split(',')
    #new=value[1:2]
    
    Light       = ''.join(value[1:2])
    Temperature = ''.join(value[3:4])
    Humidity    = ''.join(value[5:6])
    Smoke       = ''.join(value[7:8])



    Humidity    = str(Humidity)+ '%'
    Temperature = str(Temperature)+ "C"
    Luminosity  = str(Light)+ 'Lux'
    Smoke       = str(Smoke)+ '%'

    Users = {'User1':'*****','User2':'*****'}
    
    data      = {'Humidity':Humidity,'Luminosity':Luminosity,'Smoke':Smoke,'Temperature':Temperature}
    Status    ={'CR1_AC_Status': '"OFF"', 'CR1_DOOR_Status': '"OFF"', 'CR1_LIGHTS_Status': '"OFF"', 'CRA_AC1_Status':
               '"OFF"', 'CRA_AC2_Status': '"OFF"', 'CRA_DOOR_Status': '"OFF"', 'CRA_LIGHTS_Status': '"OFF"', 'WA_CAC_Status':
               '"OFF"', 'WA_CL_Status': '"OFF"', 'WA_WNDS_Status': '"OFF"', 'WB_AC1_Status': '"OFF"', 'WB_AC2_Status':
               '"OFF"', 'WB_EXHAUST_Status': '"OFF"', 'WB_LIGHTS_Status': '"OFF"', 'WC_AC_Status': '"OFF"', 'WC_OL_Status': '"OFF"', 'WC_SL_Status': '"OFF"'}
    result    = requests.get(firebase_url + '.json')
    json_data = json.loads(result.text)
    Status    ={}
    Status    = json_data["Status"]

    if len(Luminosity)>4:

      result = requests.put(firebase_url + '.json', data=json.dumps(data))
      result_Users = requests.put(firebase_url + '/Users.json', data=json.dumps(Users))
      result_Status = requests.put(firebase_url + '/Status.json', data=json.dumps(Status))
      
    print ('Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text)
 
   
  except IOError:
    print('Error! Something went wrong.')
    time.sleep(fixed_interval)



    
