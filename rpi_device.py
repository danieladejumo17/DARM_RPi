from stepper import StepperMotor


class RPiDevice:
	"""
	Controls the six stepper motor attached on the main raspberry Pi device
	"""
	def __init__(self, cmd_nsteps=1, motor_pins={0: [4,17,27,22],
								1: [10,9,11,5], 
								2: [6,13,19,26],
								3: [14,15,18,23],
								4: [24,25,8,7],
								5: [12,16,20,21]},
						motor_step_gains = [1]*6):
		
		self.cmd_nsteps = cmd_nsteps
		self.motor_pins = motor_pins
		self.motor_gains = motor_step_gains
		
		# put motors in a list
		self.create_stepper_motors()
		
	def create_stepper_motors(self):
		self.motor0 = StepperMotor(*self.motor_pins[0])
		self.motor1 = StepperMotor(*self.motor_pins[1])
		self.motor2 = StepperMotor(*self.motor_pins[2])
		self.motor3 = StepperMotor(*self.motor_pins[3])
		self.motor4 = StepperMotor(*self.motor_pins[4])
		self.motor5 = StepperMotor(*self.motor_pins[5])
		
	def act(self, cmd):
		self.motor0.step(cmd[0]*self.cmd_nsteps*self.motor_gains[0])
		self.motor1.step(cmd[1]*self.cmd_nsteps*self.motor_gains[1])
		self.motor2.step(cmd[2]*self.cmd_nsteps*self.motor_gains[2])
		self.motor3.step(cmd[3]*self.cmd_nsteps*self.motor_gains[3])
		self.motor4.step(cmd[4]*self.cmd_nsteps*self.motor_gains[4])
		self.motor5.step(cmd[5]*self.cmd_nsteps*self.motor_gains[5])
		
		# make call asynchronous








