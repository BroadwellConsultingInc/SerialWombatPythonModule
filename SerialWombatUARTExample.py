import time
import SerialWombatUART
import SerialWombatUltrasonicDistanceSensor

sw = SerialWombatUART.SerialWombatChipUART("/dev/ttyUSB0")

sw.begin(False)

print(sw.version)
print(sw.model)
print(sw.fwVersion)


distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)

distanceSensor.begin(10, # echo pin
                     0, # HC_SR04 driver
                     11) # Trigger pin





print("Source Voltage mv: ",sw.readSupplyVoltage_mV())

time.sleep(2)
while(True):
    print("Distance (mm): ",distanceSensor.readPublicData()," Pulse count: ",distanceSensor.readPulseCount())
