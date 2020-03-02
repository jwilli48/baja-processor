import accel_proxy as ap
import serial
import time
import simple_data_server as sds

s = sds.ServerFacade()
s.start_server()

ameter = ap.AccelProxy()

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate='115200',
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

packets = 0

while True:
    # read data
    x, y, z = ameter.read_xyz()
    data_str = '%0.3f %0.3f %0.3f' % (x, y, z)

    # print so pi can save data to file
    print(data_str)

    # send data
    packets = packets + 1
    ser.write(('%d ' % (packets) + data_str).encode("ascii"))

    # save to simple server
    s.save_data(data_str)

    # small delay
    time.sleep(0.2)
