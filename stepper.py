import RPi.GPIO as GPIO
import time

class StepperMotor:
	full_phase_stepping_seq = [[1,1,0,0],
							[0,1,1,0],
							[0,0,1,1],
							[1,0,0,1],
							]
	
	def __init__(self, pin1, pin2, pin3, pin4, sleep_time=0.002):
		self.pins = [pin1, pin2, pin3, pin4]
		self.sleep_time = sleep_time
		self.setup_pins()
		
		self.seq = StepperMotor.full_phase_stepping_seq
		self.current_seq_step = 0
		
		
	def setup_pins(self):
		for pin in self.pins:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, GPIO.LOW)
		
		
	def single_step(self):
		print(f"Stepping seq {self.current_seq_step}")
		for pin in range(len(self.pins)):
			GPIO.output(self.pins[pin], self.seq[self.current_seq_step][pin])
		time.sleep(self.sleep_time)
		
	def step(self, n_step):
		increment = 1 if (n_step >= 0) else -1
		for step in range(abs(n_step)):
			self.single_step()
			self.current_seq_step += increment
			self.current_seq_step = self.current_seq_step % 4
		
		
		
if __name__ == "__main__":
	GPIO.setmode(GPIO.BCM)
	
	motor = StepperMotor(6, 13, 19, 26)
	motor.step(2048)
	
	GPIO.cleanup()




