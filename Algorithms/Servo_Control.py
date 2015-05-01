#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys

# ===========================================================================
# Modification of Adafruit Script for Servo motor control.
# Original can be found at: git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
# under Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver
# Other files from that diretory are required as a dependency for servo control.
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

pwm.setPWMFreq(50)

servoMin = 150  # Min pulse length out of 4096
servo1_4 = 200
servo2_4 = 300
servo3_4 = 400

servo_t_min = 450
servo_t_mid = 500
servo_t_max = 550
servoMax = 600  # Max pulse length out of 4096

# Positions for scan
bot = True
mid = False
top = False

# This part of the script sets the PWM
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# This is the manual control algorithm, the w, a, s, d keys are used for control and go to the maximum position
# in the x or y axis.
def key_control():
  while(True):
    # Keyboard Control
    userInput = ''
    while len(userInput) != 1:
      userInput = raw_input(':')
    guessInLower = userInput.lower()  

    if guessInLower == 'w':
      pwm.setPWM(1, 0, servo_t_max)
    elif guessInLower == 's':
      pwm.setPWM(1, 0, servo_t_min)
    elif guessInLower == 'a':
      pwm.setPWM(0, 0, servo1_4)
    elif guessInLower == 'd':
      pwm.setPWM(0, 0, servo3_4)
    elif guessInLower == 'q':
      return

# This is the scan algorithm, it moves the servos from the bottom right to the top left positions
# in 3 horizontal lines, bot, mid, and top. It prints when a phase has finished on the screen.
def scan(bot, mid, top):
  # Start at bottom right and scan horizontal lines
  while(True):
    if bot == True:
      pwm.setPWM(1, 0, servo_t_min)
      time.sleep(1)
      pwm.setPWM(0, 0, servo3_4)
      time.sleep(1)
      mid = True
      bot = False
      print "bot is done"
    elif mid == True:
      pwm.setPWM(1, 0, servo_t_mid)
      time.sleep(1)
      pwm.setPWM(0, 0, servo1_4)
      time.sleep(1)
      top = True
      mid = False
      print "mid is done"
    elif top == True:
      pwm.setPWM(1, 0, servo_t_max)
      time.sleep(1)
      pwm.setPWM(0, 0, servo3_4)
      time.sleep(1)
      pwm.setPWM(0, 0, servo1_4)
      time.sleep(1)
      bot = True
      top = False
      print "top is done"
      return

# This is the main interface of the program:
# s - executes the scan algorithm
# m - switches into manual control
# q - exits the program
while (True):
  #Set servos to neutral position
  pwm.setPWM(1, 0, servo_t_min)
  time.sleep(1)
  pwm.setPWM(0, 0, servo1_4)
  time.sleep(1)

  print "Enter s to scan, or m for manual control"
  userInput = ''
  while len(userInput) != 1:
    userInput = raw_input(':')
  guessInLower = userInput.lower()  

  if guessInLower == 's':
    scan(bot, mid, top)
  elif guessInLower == 'm':
    key_control()
  elif guessInLower == 'q':
    sys.exit(0)
