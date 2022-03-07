import time

def millis():
   return (time.perf_counter_ns() /1000000)

class SerialWombatChip:
    WOMBAT_MAXIMUM_PINS = 20
    _supplyVoltagemV = 3300
    _pinmode = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # includes pullup 0 = input, 1= output, 2 = input w/ pullup
    _pullDown = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    _openDrain = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    _highLow = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sendReadyTime = 0
    lastErrorCode = 0

    def sendPacket(self,tx):
        return 8;

    def sendPacket (self,tx,rx):
        return 8,[0x55,0x55,0x55,0x55,0x55,0x55,0x55];

    def begin(self,reset = True):
        if (reset):
            self.hardwareReset();
            self._sendReadyTime = millis() + 1000
            return 1
        else:
            self._sendReadyTime = 0
            return self.initialize()

    def initialize(self):
        lastErrorCode = 0
        self.readVersion()
        self.readSupplyVoltage_mV()
        #TODO self.readUniqueIdentifier()
        #TODO self.readDeviceIdentifier()
        return(lastErrorCode)

    def readVersion(self):
        count,rx=self.sendPacket( list(bytearray("V       ", encoding = 'utf8')))
        if (count >= 0):
            self.version = rx[1:8]
            self.model = rx[1:4]
            self.fwVersion = rx[5:8]


    def readSupplyVoltage_mV(self):
        #TODO add support for SW18AB
        counts = self.readPublicData(66)
        if (counts > 0):
            mv = 1024 * 65536 / counts
            self._supplyVoltagemV = mv
        else:
            self._supplyVoltagemV = 0

        return (self._supplyVoltagemV)

    def readTemperature_100thsDegC(self):
        #TODO add support for SW18AB
        return (2500)

    def hardwareReset():
        self.sendPacket(list(bytearray("ReSeT!#*", encoding = 'utf8')))

    def pinMode(pin,mode,pullDown=False,openDrain=False):
        if (pin >= WOMBAT_MAXIMUM_PINS):
            return -32767
        self._pullDown[pin] = pullDown
        self._openDrain[pin] = openDrain
        self._pinmode[pin] = mode
        self.configureDigitalPin(pin,mode)

    def configureDigitalPin(pin, highLow):
        tx = [200,pin,0,0,0,0,0,0x55]
        if (self._pinmode[pin] == 0): #input
            tx[3] = 2 #input
        elif (self._pinmode[pin] == 1): #output
            if (highLow == 0):  #LOW
                tx[3] = 0  #low
            elif (highLow == 1):
                tx[3] = 1
            else:
                return
        elif (self._pinmode[pin] == 2 ): #pullup
            tx[3] = 2 #input
            tx[4] = 1 #Pullup on 
        else:
            return
        tx[6] = self._openDrain[pin]
        tx[5] = self._pullDowm[pin]
        self.sendPacket(tx)

    def readPublicData(self,pin):
        tx = [0x81,pin,255,255,0x55,0x55,0x55,0x55]
        count,rx = self.sendPacket(tx)
        return rx[2]+ rx[3] * 256

    def writePublicData(self,pin, value):
        tx = [0x82, pin, value & 0xFF, int(value / 256), 255, 0x55,0x55,0x55,0x55]
        count,rx = self.sendPacket(tx)
        return (rx[2] + rx[3] * 256)

    def writeUserBuffer(self,address,buf,count):
        bytesToSend = 0
        bytesSent = 0
        if (count == 0):
            return (0)
        #send first packet of up to 4 bytes
        if (count < 4):
            bytesToSend = count
            count = 0
        else:
            bytesToSend = 4
            count -= 4

        tx = [0x84,address & 0xFF, address / 256, bytesToSend, 0x55,0x55,0x55,0x55]
        for i in range (bytesToSend):
            tx[4+i] = buf[i]
        count,result = self.sendPacket(tx)
        if (count < 0):
            return (count)
        bytesSent = bytesToSend

        while (count >= 7):
            tx = [0x85,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
            for i in range(7):
                tx[i+1] = buffer[bytesSent + i]
            count,rx = self.sendPacket(tx)
            if (count < 0):
                return count
            bytesSent += 7

        while (count > 0):
            bytesToSend = 4;
            if (count < 4):
                bytesToSend = count
                count = 0
            else:
                count -=4
            a = address + bytesSent
            tx = [84,a & 0xFF, a/256,bytesToSend,0x55,0x55,0x55,0x55]
            for i in range(count):
                tx[4+i] = buf[i + bytesSent]
            count,rx = sendPacket(tx)
            if (count < 0):
                return(count)
            bytesSent += bytesToSend

        return bytesSent

    def returnErrorCode(self,rx):
        out = rx[1] - ord('0')
        out *=10;
        out += rx[2] - ord('0')
        out *=10;
        out += rx[3] - ord('0')
        out *=10;
        out += rx[4] - ord('0')
        out *=10;
        out += rx[5] - ord('0')
        return (out)




#class SerialWombatChipUART(SerialWombatChip):
