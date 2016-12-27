import time, os, thread 
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

all_inputs = []
class HwInput(object):
	def __init__(self, PIN, name):
		self.PIN = PIN
		self.name = name
		GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		all_inputs.append(self)		
		self.history = [0, 0]	

	def state(self):
		if not self.history[0] == self.history[1]:
			if self.history[1] == 1:
				return True
			elif self.history[1] == 0:
				return False
		else:
			return None
	
	def update(self):
		self.history[0] = self.history[1]
		self.history[1] = GPIO.input(self.PIN) 

	
sequence = ["" , "", "", ""]

door_sensor = HwInput(18, "door_sensor")
pressure_plate = HwInput(23, "pressure_plate")
wall_pad = HwInput(25, "wall_pad")
main_switch = HwInput(4, "main_switch")
light_state = True

def cycle(arr, item):
	arr.append(item)
	return arr[1:]

def toggleLight():
	global light_state
	light_state = not light_state	

def ioUpdate():
	global light_state, sequence
	for i in all_inputs:#updates input states
		i.update()
	
	if wall_pad.state() == True:
		toggleLight()
	if main_switch.state() == True or main_switch.state() == False:
		light_state = not light_state	
	
	
	if door_sensor.state() == True:
		sequence = cycle(sequence, "DC")#DC = Door Closed
	elif door_sensor.state() == False:
		sequence = cycle(sequence, "DO")#DO = Door Opened
	elif pressure_plate.state() == True:
		sequence = cycle(sequence, "PA")#PA = Plate Activated
	elif pressure_plate.state() == False:
		sequence = cycle(sequence, "PO")#PO = Plate Off	
		

	if sequence == ["DO", "PA", "PO", "DC"]:#could be walking in or out. Invert light state
		light_state = not light_state
		sequence = ["", "", "", ""]
	elif sequence == ["DO", "DC", "PA", "PO"]:
		light_state = True
		sequence = ["", "", "", ""]

	elif sequence == ["DO", "PA", "DC", "PO"]:
		light_state = True
		sequence = ["", "", "", ""]

	elif sequence == ["PA", "PO", "DO", "DC"]:
		light_state = False
		sequence = ["", "", "", ""]

	elif sequence == ["PA", "DO", "PO", "DC"]:
		light_state = False
		sequence = ["", "", "", ""]
	elif sequence == ["DO", "DC", "DO", "DC"]:
		light_state = False
		sequence = ["", "", "", ""]
	elif sequence == ["PA", "PO", "PA", "PO"]:
		light_state = True
		sequence = ["", "", "", ""]
		
		
	web_file = open("/var/www/html/output.txt")
	web_input = web_file.read()
	if web_input == "1":
		light_state = True
	elif web_input == "0":
		light_state = False
	web_file.close()
	
	web_file = open("/var/www/html/output.txt", "w")#clear file
	web_file.close()
	
	web_output = open("/var/www/html/state.txt", "w")
	
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
		time.sleep(0.1)


if __name__ == '__main__':
	ioUpdateLoop()
