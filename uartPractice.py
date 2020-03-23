import serial
import RPi.GPIO as IO
import time

commands = []
duty = 0

def PrintDuty():
    print('Duty Cycle is : ' + str(duty))
    
def IncreaseDuty10():
    global duty
    duty = duty + 10
    pwm.ChangeDutyCycle(duty)
    
def DecreaseDuty10():
    global duty
    duty = duty - 10
    pwm.ChangeDutyCycle(duty)
    
def SetDuty():
    global duty
    port.write('New Duty : ')
    duty = int(readLine())
    pwm.ChangeDutyCycle(duty)

def convert(l) : # convert list of chars to string
    s = ""
    for c in l :
        s += c
    return s
    
def readLine():
    global line
    line = []
    while True :
        for c in port.read() :
            port.write(c)
            if c == '\n' or c == '\r':
                port.write('\r\n')
                return convert(line) #returns a string, not a list
            if c == '\x08' : #Backspace
                port.write(' ') #erase last letter from screen
                port.write(c)
                line.pop() # erase last letter from 'list'
            else :
                line.append(c)
    
def InterpretCommand(cmd):
    a = 0 #index of command
    for i in range(len(commands)) :
        if str(commands[i]) == cmd :
            a = i + 1
            break
    print(a) 
    switcher = {
        1 : PrintDuty,
        2 : IncreaseDuty10,
        3 : DecreaseDuty10,
        4 : SetDuty
    }
    func = switcher.get(a, lambda: "Invalid Command")
    func()
    
def readBT():
    global port
    global line
    cmd = readLine() # updates 'line'
    InterpretCommand(cmd) # calls its corresponding function
    
def commandsInit():
    commands.append('PrintDuty')
    commands.append('IncreaseDuty10')
    commands.append('DecreaseDuty10')
    commands.append('SetDuty')    
    
def PWMsetup(pin, freq):
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(pin, IO.OUT)
    p = IO.PWM(pin, freq)
    p.start(0)
    return p
    
def UARTsetup():
    port = serial.Serial("/dev/ttyS0", baudrate = 9600, timeout = 3.0)
    port.close()
    port.open()
    port.write('Starting UART connection...\r\n')
    return port
    
port = UARTsetup()
pwm = PWMsetup(19,100)
line = []
def main(args):
    commandsInit()
    while True:
        readBT()
            
            
    
    return 0
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))