
# Serial to Firebase Data Logger

This project reads sensor data from a serial port and logs the data to Firebase in real-time. The sensor data includes light intensity, temperature, humidity, and smoke levels.

## Prerequisites

- Python 3.x
- `pyserial` library
- `requests` library

You can install the required libraries using pip:

```bash
pip install pyserial requests
```

## Setup

1. **Configure Firebase URL**:
   - Replace the placeholder `firebase_url` in the code with your actual Firebase URL.

2. **Connect to Serial Port**:
   - Ensure your sensor device is connected to the serial port (e.g., `COM7` on Windows). Adjust the serial port settings (`COM7`, `115200`) as per your device's configuration.

## Usage

1. **Run the Script**:
   - Execute the script to start reading data from the serial port and uploading it to Firebase.

```bash
python serial_to_firebase.py
```

## Code Explanation

### Connecting to Firebase

```python
# Connection to Firebase
firebase_url = '****************'
```

Replace the placeholder with your actual Firebase URL.

### Serial Port Configuration

```python
# Connect to Serial Port for communication
ser = serial.Serial('COM7', 115200, timeout=0)
```

Ensure the serial port and baud rate match your device's settings.

### Main Loop

The script continuously reads data from the serial port, processes the data, and uploads it to Firebase.

```python
while True:
    try:
        # Read all characters in buffer from the serial port
        msg = ser.readline()
        
        # Decode message and split by commas
        value = msg.decode('ascii').strip().split(',')

        # Extract and format sensor values
        Light = ''.join(value[1:2])
        Temperature = ''.join(value[3:4])
        Humidity = ''.join(value[5:6])
        Smoke = ''.join(value[7:8])

        Humidity = str(Humidity) + '%'
        Temperature = str(Temperature) + 'C'
        Luminosity = str(Light) + 'Lux'
        Smoke = str(Smoke) + '%'

        # User data (obfuscated)
        Users = {'User1': '*****', 'User2': '*****'}

        # Data to be sent to Firebase
        data = {
            'Humidity': Humidity,
            'Luminosity': Luminosity,
            'Smoke': Smoke,
            'Temperature': Temperature
        }

        # Initialize status dictionary
        Status = {
            'CR1_AC_Status': '"OFF"',
            'CR1_DOOR_Status': '"OFF"',
            'CR1_LIGHTS_Status': '"OFF"',
            'CRA_AC1_Status': '"OFF"',
            'CRA_AC2_Status': '"OFF"',
            'CRA_DOOR_Status': '"OFF"',
            'CRA_LIGHTS_Status': '"OFF"',
            'WA_CAC_Status': '"OFF"',
            'WA_CL_Status': '"OFF"',
            'WA_WNDS_Status': '"OFF"',
            'WB_AC1_Status': '"OFF"',
            'WB_AC2_Status': '"OFF"',
            'WB_EXHAUST_Status': '"OFF"',
            'WB_LIGHTS_Status': '"OFF"',
            'WC_AC_Status': '"OFF"',
            'WC_OL_Status': '"OFF"',
            'WC_SL_Status': '"OFF"'
        }

        # Retrieve current status from Firebase
        result = requests.get(firebase_url + '.json')
        json_data = json.loads(result.text)
        Status = json_data["Status"]

        # If the Luminosity value is valid (length > 4), update Firebase
        if len(Luminosity) > 4:
            result = requests.put(firebase_url + '.json', data=json.dumps(data))
            result_Users = requests.put(firebase_url + '/Users.json', data=json.dumps(Users))
            result_Status = requests.put(firebase_url + '/Status.json', data=json.dumps(Status))

        # Print result of the operation
        print('Record inserted. Result Code = ' + str(result.status_code) + ', ' + result.text)

    except IOError:
        # Handle errors and wait for the next interval
        print('Error! Something went wrong.')
        time.sleep(fixed_interval)
```

### Error Handling

If an error occurs during data reading or writing to Firebase, it is caught and a message is printed. The script then waits for the specified interval before attempting to read the data again.

```python
except IOError:
    # Handle errors and wait for the next interval
    print('Error! Something went wrong.')
    time.sleep(fixed_interval)
```

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Pyserial](https://pyserial.readthedocs.io/en/latest/)
- [Requests](https://requests.readthedocs.io/en/latest/)