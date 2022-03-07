import SerialWombatPin

class SerialWombatServo (SerialWombatPin.SerialWombatPin):
    _min = 544
    _max = 2400
    _reverse = 0
    _position = 0

    def __init__(self,sw):
        self._sw = sw


    def attach(self,pin, minimum=544, maximum = 2400, reverse = False):
        self._pin = pin
        self._min = minimum
        self._max = maximum
        if (reverse):
            self._reverse = 1
        else:
            self._reverse = 0
        self._pinMode =  3 # Servo

        tx = [200, self._pin, self._pinMode,self._pin,self._position & 0xFF, int(self._position / 256), self._reverse,0x55]

        self._sw.sendPacket(tx)
        duration = self._max - self._min
        tx2 = [201, self._pin, self._pinMode,self._min & 0xFF, int(self._min / 256), duration & 0xFF, int(duration / 256) ,0x55,0x55]
        self._sw.sendPacket(tx2)

    def write16bit(self,position):
        self._position = int(position)
        self.writePublicData(self._position)

    def write(self,angle):
        if (angle < 180):
            self.write16bit(int(65536 * angle / 180))
        else:
            self.write16bit(65535)

    def read(self):
        returnval = self._position * 180 / 65536
        return int(returnval)



