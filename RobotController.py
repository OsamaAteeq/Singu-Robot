import serial
import keyboard
import time
import threading

# Set this to your Arduino COM port (check Arduino IDE)
arduino = serial.Serial('COM8', 9600)  # e.g., 'COM4' or '/dev/ttyUSB0'
time.sleep(2)  # wait for Arduino to reset

print("FOR HEAD : Press A (LEFT), D (Right)")
print("FOR ARM1 :  Press F (LEFT), H (Right)")
print("FOR ARM2 :  Press J (LEFT), L (Right)")
print("FOR ARMS :  Press N (LEFT), M (Right)")
print("DANCE 1 :  Press Z")
print("Press Q (quit)")

last_cmd = None
arm_locked = False  # Global flag
head_locked = False # Global flag
arm2Angle = 0
arm1Angle = 0
headAngle = 0

def dance1 ():
    global arm_locked
    global arm2Angle
    global arm1Angle
    arm_locked = True
    print("DANCE 1")
    for _ in range(2):
        while (arm1Angle < 50 or arm2Angle < 50):
            if arm1Angle < 50:
                arduino.write(b'h')
                arm1Angle += 10
            if arm2Angle < 50:
                arduino.write(b'l')
                arm2Angle += 10
        while (arm1Angle > 0 or arm2Angle > 0):
            if arm1Angle > 0:
                arduino.write(b'f')
                arm1Angle -= 10
            if arm2Angle > 0:
                arduino.write(b'j')
                arm2Angle -= 10
    arm_locked = False

def dance2 ():
    global arm_locked
    global arm2Angle
    global arm1Angle
    arm_locked = True
    print("DANCE 2")
    while (arm1Angle < 50):
        arduino.write(b'f')
        arm1Angle += 10

    for _ in range(2):
        while (arm1Angle > 0 or arm2Angle < 50):
            if arm2Angle < 50:
                arduino.write(b'j')
                arm2Angle += 10
            if arm1Angle > 0:
                arduino.write(b'h')
                arm1Angle -= 10
        while (arm2Angle > 0 or arm1Angle < 50):
            if arm1Angle < 50:
                arduino.write(b'f')
                arm1Angle += 10
            if arm2Angle > 0:
                arduino.write(b'l')
                arm2Angle -= 10
    
    while (arm1Angle > 0):
        arduino.write(b'h')
        arm1Angle -= 10
    arm_locked = False

def sad ():
    global head_locked
    global headAngle
    head_locked = True
    print("SAD")
    for _ in range(3):
        while (headAngle < 600):
            arduino.write(b'a')
            headAngle += 30
        while (headAngle > -600):
            arduino.write(b'd')
            headAngle -= 30

    while (headAngle < 0):
            arduino.write(b'a')
            headAngle += 30
    head_locked = False

try:
    while True:
        #HEAD
        if not head_locked:
            if keyboard.is_pressed('a'):
                arduino.write(b'a')
                if last_cmd != 'a':
                    print("HeadLeft")
                last_cmd = 'a'
            elif keyboard.is_pressed('d'):
                arduino.write(b'd')
                if last_cmd != 'd':
                    print("HeadRight")
                last_cmd = 'd'
        if not arm_locked:
            #ARM1
            if keyboard.is_pressed('f'):
                arduino.write(b'f')
                if last_cmd != 'f':
                    print("ARM1Left")
                last_cmd = 'f'
            elif keyboard.is_pressed('h'):
                arduino.write(b'h')
                if last_cmd != 'h':
                    print("ARM1Right")
                last_cmd = 'h'
            #ARM2
            if keyboard.is_pressed('j'):
                arduino.write(b'j')
                if last_cmd != 'j':
                    print("ARM2Left")
                last_cmd = 'j'
            elif keyboard.is_pressed('l'):
                arduino.write(b'l')
                if last_cmd != 'l':
                    print("ARM2Right")
                last_cmd = 'l'

            #BOTH
            if keyboard.is_pressed('n'):
                arduino.write(b'f')
                arduino.write(b'j')
                if last_cmd != 'n':
                    print("BOTH ARMS Left")
                last_cmd = 'n'

            elif keyboard.is_pressed('m'):
                arduino.write(b'h')
                arduino.write(b'l')
                if last_cmd != 'm':
                    print("BOTH ARMS RIGHT")
                last_cmd = 'm'
        #DANCE 1
        if keyboard.is_pressed('z') and not arm_locked:
            threading.Thread(target=dance1, daemon=True).start()
            time.sleep(0.1)
            last_cmd = 'z'

        #DANCE 2
        if keyboard.is_pressed('c') and not arm_locked:
            threading.Thread(target=dance2, daemon=True).start()
            time.sleep(0.1)
            last_cmd = 'c'
            
        #Sad
        if keyboard.is_pressed('x') and not head_locked:
            threading.Thread(target=sad, daemon=True).start()
            time.sleep(0.1)
            last_cmd = 'x'

        #QUIT
        if keyboard.is_pressed('q'):
            print("Exiting...")
            break

       
        time.sleep(0.2)
        if (not (keyboard.is_pressed('a') or keyboard.is_pressed('d')) and not head_locked):
            arduino.write(b's')
        if (not (keyboard.is_pressed('f') or keyboard.is_pressed('h')) and not arm_locked):
            arduino.write(b'g')
        if not ((keyboard.is_pressed('j') or keyboard.is_pressed('l')) and not arm_locked):
            arduino.write(b'k')

except KeyboardInterrupt:
    pass

arduino.close()

