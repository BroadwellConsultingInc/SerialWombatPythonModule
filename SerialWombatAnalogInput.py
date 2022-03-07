import SerialWombatPin

class SerialWombatAnalogInput (SerialWombatPin.SerialWombatPin):
    def __init__(self,sw):
        self._sw = sw

    def begin(self,pin,averageSamples=64,filterConstant = 0xFF80, output = 0):
        self._pin = pin
        self._pinMode = 2 #Analog input
        tx = [200,self._pin,self._pinMode, 0,0,0,0,0]
        count,rx = self._sw.sendPacket(tx)
        if (count < 0):
            return count
        tx = [201,self._pin,self._pinMode, averageSamples & 0xFF, int(averageSamples / 256),filterConstant& 0xFF, int(filterConstant / 256),output]
        count,rx = self._sw.sendPacket(tx)
        self.updateSupplyVoltage_mV()
        return count

    def readVoltage_mV(self):
        reading = self.readPublicData()
        reading *= self._sw._supplyVoltagemV
        reading/= 65536
        return (reading)

    def readCounts(self):
        return self.readPublicData()

    def readFiltered_mV(self):
        x = self.readFilteredCounts()
        if (x < 0):
            return (0)
        x *= self._sw._supplyVoltagemV
        x /= 65536
        return (x)

    def readFilteredCounts(self):
        tx = [204, self._pin, self._pinMode, 0x55,0x55,0x55,0x55,0x55]
        count,rx = _sw.sendPacket(tx)
        if (count < 0):
            return 0
        return (rx[5] + 256 * rx[6])

    def readAveragedCounts_mV(self):
        x = self.readAveragedCounts()
        if (x < 0):
            return (0)
        x *= self._sw._supplyVoltagemV
        x /= 65536
        return (x)


    def readAveragedCounts(self):
        tx = [204, self._pin, self._pinMode, 0x55,0x55,0x55,0x55,0x55]
        count,rx = _sw.sendPacket(tx)
        if (count < 0):
            return 0
        return (rx[3] + 256 * rx[4])

    def updateSupplyVoltage_mV(self):
        return self._sw.readSupplyVoltage_mV()

    def readMaximumCounts_mV(self, resetAfterRead = False):
        x = self.readMaximumCounts(resetAfterRead)
        x *= self._sw._supplyVoltagemV
        x /= 65536
        return (x)


    def readMaximumCounts(self,resetAfterRead = False):
        tx = [203, self._pin, self._pinMode, 0x55,0x55,0x55,0x55,0x55]
        if (resetAfterRead):
            tx[3] = 1

        count,rx = _sw.sendPacket(tx)
        if (count < 0):
            return 0
        return (rx[5] + 256 * rx[6])

    def readMinimumCounts_mV(self, resetAfterRead = False):
        x = self.readMinimumCounts(resetAfterRead)
        x *= self._sw._supplyVoltagemV
        x /= 65536
        return (x)

    def readMinimumCounts(self,resetAfterRead = False):
        tx = [203, self._pin, self._pinMode, 0x55,0x55,0x55,0x55,0x55]
        if (resetAfterRead):
            tx[3] = 1

        count,rx = _sw.sendPacket(tx)
        if (count < 0):
            return 0
        return (rx[3] + 256 * rx[4])






    

