import time
import serial
import array
import paho.mqtt.client as mqtt

print("Connecting to broker...")

status = False

client = mqtt.Client("MicNum")
client.username_pw_set(username="homeassistant", password="quee6Zea3zoeb8tieghaNuwu4Jahk9phoogohphahpieF4oKi3zaiY6loh8sedog")

while status == False:
    try:
        client.connect("10.110.15.57", 1883, 3600)
        status = True
        print("Connected to broker")
    except:
        pass

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=0,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()

print("connected to: " + ser.portstr)

while True:
    bytesToRead = ser.inWaiting()
    data = ser.read(bytesToRead)
    time.sleep(0)
    if len(data) != 0:
        x = array.array('B', data)
        if len(x) >= 8:
            micnum = x[-2]
            print(micnum)
            client.publish('mic/num', micnum)
            rc = str(client.publish('mic/num', micnum))[1]
            print("rc: " + rc)
            if int(rc) != 0:
                print("reconnect")
                client.reconnect()
                client.publish('mic/num', micnum)
