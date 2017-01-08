import time
from threading import Timer
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

def cycle(arr, item):
	arr.append(item)
	return arr[1:]

all_inputs = []
class HwInput(object):
	def __init__(self, PIN, name):
		self.PIN = PIN
		self.name = name
		GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		all_inputs.append(self)		
		self.history = [0, 0]	

	def state(self):#state() returns the change of input
			#True = [0, 1] = stepped on
			#False = [1, 0] = stepped off
			#None = No change
		if not self.history[0] == self.history[1]:
			if self.history[1] == 1:
				return True
			elif self.history[1] == 0:
				return False
		else:
			return None
	
	def update(self):
		self.history = cycle(self.history, GPIO.input(self.PIN))
		
sequence = []
for i in range(2):
	sequence.append("")

door_sensor = HwInput(18, "door_sensor")
pressure_plate = HwInput(23, "pressure_plate")
wall_pad = HwInput(25, "wall_pad")
main_switch = HwInput(4, "main_switch")
door_laser = HwInput(17, "door_laser")
light_state = True #light is on by default
laser_state = False #laser is not tripped by default


def coolDownFunction():
	global sequence
	print("sequence cleared due to cool down")
	sequence = ["", ""]

def restartCoolDownTimer():
	global cool_down_timer
	cool_down_timer.cancel()
	cool_down_timer = Timer(8, coolDownFunction)
	cool_down_timer.start()
	
cool_down_timer = Timer(8, coolDownFunction)



def toggleLight():
	global light_state
	light_state = not light_state	

def ioUpdate():
	global light_state, sequence, cool_down_timer
	for i in all_inputs:
		i.update()
	
	print(sequence)
		
	if wall_pad.state() == True:#When wall pad is pressed toggle light
		toggleLight()
	if main_switch.state() == True or main_switch.state() == False:#when light switch changes, toggle light
		toggleLight()
	
	if pressure_plate.state() == True:
		sequence = cycle(sequence, "PA")#PA = Plate Activated
		restartCoolDownTimer()

	elif door_laser.state() == True:
		sequence = cycle(sequence, "LT")#LT = Laser Triggered		
		restartCoolDownTimer()



	if sequence == ["LT", "PA"]:
		if light_state == False:		
			light_state = True
		#sequence = ["", ""]
		
	elif sequence == ["PA", "LT"]:
		if light_state == True:
			light_state = False
		#sequence = ["", ""]
		
				
	
	web_file = open("/var/www/html/output.txt")#output from web client
	web_input = web_file.read()
	if web_input == "1":
		light_state = True
	elif web_input == "0":
		light_state = False
	web_file.close()
	
	web_file = open("/var/www/html/output.txt", "w")#clear file
	web_file.close()
	
	web_output = open("/var/www/html/state.txt", "w")#output to web client
	
	if light_state == True:
		GPIO.output(24, False)
		web_output.write("on")
	else:
		GPIO.output(24, True)
		web_output.write("off")
	
	web_output.close()


def ioUpdateLoop():
	while True:
		ioUpdate()
		time.sleep(0.025)


if __name__ == '__main__':
	ioUpdateLoop()
