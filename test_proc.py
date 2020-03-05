import time
import simple_data_server as sds

s = sds.ServerFacade()
s.start_server()

packets = 0

while True:
    # read data
    x, y, z = (0.5, 0.2, 0.3)
    data_str = '%0.3f %0.3f %0.3f' % (x, y, z)

    # print so pi can save data to file
    print(data_str)

    # send data
    packets = packets + 1

    # save to simple server
    s.save_data(data_str)

    # small delay
    time.sleep(0.2)
