import board
import digitalio
import busio
import adafruit_lis3dh


class AccelProxy:
    def __init__(self, g_range=adafruit_lis3dh.RANGE_2_G):
        # Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
        # otherwise check I2C pins.
        if hasattr(board, 'ACCELEROMETER_SCL'):
            i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
            int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
            self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(
                i2c, address=0x19, int1=int1)
        else:
            i2c = busio.I2C(board.SCL, board.SDA)
            # Set to correct pin for interrupt!
            int1 = digitalio.DigitalInOut(board.D6)
            self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

        self.lis3dh.range = g_range

    def read_xyz(self):
        x, y, z = [
            value / adafruit_lis3dh.STANDARD_GRAVITY for value in self.lis3dh.acceleration]
        return (x, y, z)
