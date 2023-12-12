import SerialWombatPin

class SerialWombatPWM (SerialWombatPin.SerialWombatPin):

    _dutyCycle = 0
    def __init__(self,sw):
        self._sw = sw

    def begin(self,pin, dutyCycle = 0, invert = False):
        self._pin = pin
        self._pinMode =  16 # PWM

        tx = [200, self._pin, self._pinMode,self._pin,dutyCycle & 0xFF, int(dutyCycle / 256), invert,0x55]
        self._sw.sendPacket(tx)

    def writeDutyCycle(self,dutyCycle):
        self.writePublicData(self.dutyCycle)


class SerialWombatPWM_4AB (SerialWombatPWM):
    def setFrequency_SW4AB(frequencyEnum):
        tx = [220, self._pin, frequencyEnum,0x55,0x55,0x55,0x55]
        self._sw.sendPacket(tx)

class SerialWombatPWM_18AB (SerialWombatPWM):
    def writePeriod_uS(self, period_uS):
        tx = [220, self._pin, int(period_uS / (256*256*256)),int(period_uS / (256*256))& 0xFF,int(period_uS / (256))& 0xFF, period_uS & 0xFF),0x55]
        self._sw.sendPacket(tx)

    def writeFrequency_Hz(self, frequency_Hz):
        self.writePeriod_uS(int(1000000/frequency_Hz))

