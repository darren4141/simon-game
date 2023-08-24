from machine import Pin,Timer,I2C,PWM
from time import sleep
import random

notes = [262, 330, 392, 523]
sequence = []

speaker = PWM(Pin(16))

ledPins = [9, 8, 7, 6]
buttonPins = [13, 12, 11, 10]

numButtons = len(buttonPins)

led = []
button = [Pin(13, Pin.IN, Pin.PULL_UP), Pin(12, Pin.IN, Pin.PULL_UP), Pin(11, Pin.IN, Pin.PULL_UP), Pin(10, Pin.IN, Pin.PULL_UP)]

for i in ledPins:
    led.append(Pin(i, Pin.OUT))
    
for i in range(0, 4):
    led[i].low()

def playnote(frequency, Duration):
    if frequency == "0":
        sleep(Duration)
    elif frequency != "0":
        speaker.duty_u16(0)
        sleep(0.05)
        speaker.duty_u16(1500)
        speaker.freq(frequency)
        sleep(Duration)

def recordMoves(score):
    moves = []
    done = False
    times = 0
    quiet = 0
    
    while not done:
        for i in range (0, numButtons):
            if button[i].value() == 0:
                quiet = 0
                led[i].high()
                playnote(notes[i], 0.5)
                led[i].low()              
                times += 1
                moves.append(i)
            elif button[i].value() == 1:
                quiet += 1
                
        if times >= score:
            done = True
            return moves
        
        if quiet > 75000:
            done = True
            print("out of time")
            return [5]

def setMoves(score):
    global sequence
    sequence.append(random.randrange(0, 4))
    
    for v in sequence:
        led[v].high()
        playnote(notes[v], 0.5)
        led[v].low()
        sleep(0.2)

def startAnimation():
    for i in range(0, 4):
        led[i].high()
        playnote(notes[i], 0.5)
        led[i].low()
        sleep(0.2)
    speaker.duty_u16(0)

        
def loseAnimation():
    
    for j in range(0, 3):
        for i in range(0, 4):
            led[i].high()
        playnote(294, 0.3)
        for i in range(0, 4):
            led[i].low()
        sleep(0.3)
    speaker.duty_u16(0)
    
def startGame():
    global sequence
    sequence.clear()
    lose = False
    score = 1

    while not lose:
        sleep(1)
        setMoves(score)
        recorded = recordMoves(score)
        score += 1
        if recorded != sequence:
            lose = True
            print("You lose! Score: ", score-2)
            loseAnimation()
            
            
startAnimation()

while True:
    if button[0].value() == 0:
        startGame()

