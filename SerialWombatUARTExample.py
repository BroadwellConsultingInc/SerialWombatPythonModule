import time
import RPi.GPIO as GPIO
import SerialWombatUART
import SerialWombatServo
import SerialWombatAnalogInput
import SerialWombatQuadEnc


GPIO.setwarnings(False)

sw = SerialWombatUART.SerialWombatChipUART("/dev/ttyUSB0")

sw.begin(False)

print(sw.version)
print(sw.model)
print(sw.fwVersion)



analog0 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog1 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog2 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog3 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog4 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog16 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog17 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog18 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog19 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
analog0.begin(0)
analog1.begin(1)
analog2.begin(2)
analog3.begin(3)
analog4.begin(4)
analog16.begin(16)
analog17.begin(17)
analog18.begin(18)
analog19.begin(19)




print("Source Voltage mv: ",sw.readSupplyVoltage_mV())

time.sleep(2)
while(True):
    print("0: ",analog0.readCounts(), " 1: ", analog1.readCounts(), " 2: ", analog2.readCounts(), " 3: ", analog3.readCounts(), " 4: ", analog4.readCounts(),
          " 16: ", analog16.readCounts(), " 17: ", analog17.readCounts(), " 18: ", analog18.readCounts(), " 19: ", analog19.readCounts())
