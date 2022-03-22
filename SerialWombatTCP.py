import SerialWombat
import time
import socket
import select



class SerialWombatChipTCP(SerialWombat.SerialWombatChip):
    ser  = 0
    def __init__(self,host, port):
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.connect((host,port))
        self.ser.setblocking(0)


    def sendPacket (self,tx):
        clear = [0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
        self.ser.sendall(bytearray(clear))
        time.sleep(0.002)

        ready = select.select([self.ser],[],[],0)
        while (ready[0]):
            rx = self.ser.recv( 1)
            ready = select.select([self.ser],[],[],0)
        self.ser.sendall(bytearray(tx))
        time.sleep(0.002)
        rx = []
        delaycount = 0
        while (len(rx) < 8 and delaycount < 25):
            ready = select.select([self.ser],[],[],0)
            while (ready[0]):
                newBytes = self.ser.recv(1)
                rx += newBytes
                ready = select.select([self.ser],[],[],0)
            time.sleep(.002)
            ++ delaycount
        return 8,bytearray(rx)  #TODO add error check, size check

