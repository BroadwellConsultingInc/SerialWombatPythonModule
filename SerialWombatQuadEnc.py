import SerialWombatPin

class SerialWombatQuadEnc (SerialWombatPin.SerialWombatPin):
    def __init__(self,sw):
        self._sw = sw

    def begin(self,pin,secondPin,debounce_mS = 10,pullUpsEnabled = True, readState = 6): #6 = both, polling
        self._pin = pin
        self._pinMode = 5 #Quadrature Encoder
        tx = [200,self._pin,self._pinMode, debounce_mS & 0xFF,int(debounce_mS/256),secondPin,readState,int(pullUpsEnabled == True)]
        count,rx = self._sw.sendPacket(tx)
        return count

    def read(self,replacementValue = None):
        if (replacementValue is None):
            return self.readPublicData()
        return self.writePublicData(replacementValue)

    def write(self,value):
        count,rx = self.writePublicData(value)
        return count


