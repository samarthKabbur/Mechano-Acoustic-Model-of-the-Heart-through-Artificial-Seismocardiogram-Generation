# The frequencies in this code was based on the note frequencies found at:
# https://pages.mtu.edu/~suits/notefreqs.html
# Tuned at A4 = 440Hz.
 
import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pin7 = GPIO.PWM(7, 100)
pin7.start(50)
 
while True:
  GPIO.output(7, GPIO.HIGH)
  pin7.ChangeFrequency(16.35) # C0
  sleep(1)
  pin7.ChangeFrequency(261.63) # C4
  sleep(1)
  pin7.ChangeFrequency(293.66) # D4
  sleep(1)
  pin7.ChangeFrequency(329.63) # E4
  sleep(1)
  pin7.ChangeFrequency(349.23) # F4
  sleep(1)
  pin7.ChangeFrequency(392.00) # G4
  sleep(1)
  pin7.ChangeFrequency(440.00) # A4
  sleep(1)
  pin7.ChangeFrequency(493.88) # B4
  sleep(1)
  pin7.ChangeFrequency(523.25) # A5
  sleep(1.5)
  pin7.ChangeFrequency(16.35) # C0
  sleep(1)
  GPIO.output(7, GPIO.LOW)
  sleep(1)
