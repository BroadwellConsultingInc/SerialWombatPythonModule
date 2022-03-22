import SerialWombat
import time
import serial



class SerialWombatChipUART(SerialWombat.SerialWombatChip):
    ser  = 0
    def __init__(self,portname):
        self.ser = serial.Serial(portname,115200,timeout=0)


    def sendPacket (self,tx):
        clear = [0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
        self.ser.write(clear)
        time.sleep(0.002)
        rx = self.ser.read(size=8) 
        while (len(rx) > 0):
            rx = self.ser.read(size = 1)
        self.ser.write(tx)
        time.sleep(0.002)
        rx = self.ser.read(size=8) 
        delaycount = 0
        while (len(rx) < 8 and delaycount < 25):
            newBytes = self.ser.read(size = 8 - len(rx))
            if (len(newBytes) > 0):
                rx += newBytes
            time.sleep(.002)
            ++ delaycount
        return 8,rx  #TODO add error check, size check

