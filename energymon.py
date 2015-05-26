#! /usr/bin/python
# This is the Meeuwenstraat Energy Monitor
# Listens to the serial data from P1 port of DSMR meters
# Currently setup for DSMR 4.0

print "Meeuwenstraat Energy Monitor"

import serial, atexit, Queue, threading, sys, time, re, json, requests

# Atexit
def exithandler():
    if(ser.isOpen()):
        ser.close()
    print "Closed %s" % ser.name

atexit.register(exithandler)

# Setup serial port and settings
state_hist_max = 12;
state_post_url = 'http://tomlankhorst.nl/energy/post.php';
time_between_store = 300;

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=1
ser.rtscts=0
ser.timeout=20

# Open COM port
def opencomport(): 
    try:
        ser.open()
    except:
        sys.exit ("Error opening %s."  % ser.name)
    print "Opened %s" % ser.name

opencomport()

# State archiver
state_hist = []
last_state_store = 0;

def store_state ( state ) :
    global state_hist
    global last_state_store

    if state['time'] - last_state_store < time_between_store:
        return
    else:
        last_state_store = state['time']

    state_hist.append(state.copy())
    if len(state_hist) > state_hist_max:
        state_json = json.dumps(state_hist)
        r = requests.post(state_post_url, data={'state': state_json})
        print r.text
        state_hist = []


# Reader thread
def serial_reader():

    # State dict
    state = {'time': None, 'energy_t1': None, 'energy_t2': None, 'power': None, 'gas': None}

    while True:
        line = ser.readline()
        keys = re.search('[0-9]-[0-9]:[0-9]+\.[0-9]+\.[0-9]+', line)
        if not keys: 
            continue

        vals = re.search('\([0-9]+\.[0-9]+\*', line);
        if not vals:
            continue

        v = float(vals.group(0)[2:-1])

        k = keys.group(0)
        if k == '1-0:1.8.1':
            # Used energy T1
            state['energy_t1'] = v
        elif k == '1-0:1.8.2':
            # Used energy T2
            state['energy_t2'] = v
        elif k == '1-0:1.7.0': 
            # Currently consuming
            state['power'] = v
        elif k == '0-1:24.2.1':
            # Used gas volume
            state['gas'] = v
            # This is the last form the list
            state['time'] = int(time.time())
            if not None in state.values():
                store_state( state )

# Start the reading thread
try:
    t = threading.Thread( target=serial_reader )
    t.daemon = True
    t.start()

    # Just sleep, stand by and enjoy the show
    while True: time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    sys.exit("Bye bye!");
