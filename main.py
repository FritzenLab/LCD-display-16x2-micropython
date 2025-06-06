from machine import Pin, SoftI2C, I2C, ADC
from machine_i2c_lcd import I2cLcd
import time
from time import sleep

led = machine.Pin(15, machine.Pin.OUT)
button= machine.Pin(16, machine.Pin.IN)

LM35 = ADC(Pin(26)) #ADC0
initialtime = 0
LM35C= 0
counter= 0
display= 0

buttontime= time.ticks_ms()
counting= 0
ledon= False
laststate= 1
buttonon= False
clicks= 0
    
# Define the LCD I2C address and dimensions
I2C_ADDR = 0x3D
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(id=0, scl=5, sda=4, freq=400_000)
devices = i2c.scan()
print("I2C devices:", [hex(d) for d in devices])

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

try:
    while True:
        currenttime= time.ticks_ms() #Every time it passes here, gets the current time
        if time.ticks_diff(time.ticks_ms(), initialtime) > 100: # this IF will be true every 100 ms
            initialtime= time.ticks_ms() #update with the "current" time
            display= display + 1
            if(display > 9): #display is updated every 10x 100ms
                display= 0
                counter= counter + 1
                # Clear the LCD
                lcd.clear()
                # Display two different messages on different lines
                # By default, it will start at (0,0) if the display is empty
                lcd.putstr("Temp= ");
                lcd.move_to(6, 0)
                lcd.putstr(str(LM35C)+ " C")
                # Starting at the second line (0, 1)
                lcd.move_to(0, 1)
                lcd.putstr("Sec= ")
                lcd.move_to(4, 1)
                lcd.putstr(str(counter))
                
                lcd.move_to(9, 1)
                lcd.putstr("LED=")
                lcd.move_to(13, 1)
                if (ledon):
                    lcd.putstr("on")
                else:
                    lcd.putstr("off")
                
                
                LM35raw = LM35.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
                # line below converts from 16bit to volts, then rounds it to 3 places then
                # multiplies by 100 to convert from milivolts to degrees Celsius
                LM35C= round((LM35raw * 3.3 / 65535),3)*100 
                print(LM35C, end= "")
                print(" C")
                
             

            if time.ticks_diff(time.ticks_ms(), buttontime) > 20: # this IF will be True every 20 ms
                buttontime= time.ticks_ms() 
                
                if button.value() == 1 and laststate == 0:
                    clicks+= 1
                    print("LED state changed")
                    print("clicks: " + str(clicks))
                    laststate= 1
                    ledon = not ledon
                    buttonon= True
                    led.value(ledon) 
                
                    
                if buttonon == True and counting < 20:
                    counting+= 1
                    
                else:
                    counting= 0
                    buttonon= False
                    laststate= 0
                
                                

except KeyboardInterrupt:
    # Turn off the display
    print("Keyboard interrupt")
    lcd.backlight_off()
    lcd.display_off()
