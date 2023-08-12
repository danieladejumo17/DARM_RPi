from typing import Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import pprint

from rpi_device import RPiDevice
from pico_device import PicoDevice

import RPi.GPIO as GPIO


class DARMRPiController:
	def __init__(self):
		# Process actuator command from user
		# Manages 1 RPiDevice and 6 PicoDevice(s)
		
		print("Done Initializing all devices")
		
		self.rpi_device = RPiDevice(cmd_nsteps=1, motor_pins={0: [4,17,27,22],
																1: [10,9,11,5], 
																2: [6,13,19,26],
																3: [14,15,18,23],
																4: [24,25,8,7],
																5: [12,16,20,21]},
									motor_step_gains = [5]*6)
		
		self.rpi_motors = [["ii", "Exensor Communis", 1],
								["iii", "Exensor Communis", -1],
								["iv", "Exensor Communis", -1],
								["i", "Abductor Pollicis Longus", 1],
								["i", "Extensor Pollicis Brevis", 1],
								["i", "Extensor Pollicis Longus", 1]]
								
		self.rpi_motors = [["ii", "Exensor Communis", 1],
								["ii", "Flexor Profundus", -1],
								["ii", "Flexor Superficialis", +1],
								["i", "Abductor Pollicis Longus", 1],
								["ii", "Palmar Interossei", 1],
								["ii", "Dorsal Interossei", -1]]
                              
		self.pico_dev1_motors = [["iii", "Flexor Profundus", 1],
										["iii", "Flexor Superficialis", 1],
										["iii", "Dorsal Interossei", -1],
										["iii", "Palmar Interossei", -1],
										["iv", "Flexor Profundus", 1],
										["iv", "Dorsal Interossei", -1]]
										
		self.pico_dev2_motors = [["ii", "Flexor Profundus", -1],
										["ii", "Flexor Superficialis", 1],
										["ii", "Dorsal Interossei", -1],
										["ii", "Palmar Interossei", 1],
										["iv", "Flexor Superficialis", 1],
										["iv", "Palmar Interossei", -1]]
										
		self.pico_dev3_motors = [["v", "Flexor Profundus", 1],
										["v", "Flexor Superficialis", -1],
										["v", "Dorsal Interossei", 1],
										["v", "Palmar Interossei", 1],
										["v", "Opponens Digiti Minimi", -1],
										["v", "Exensor Communis", -1]]
                             
		self.pico_dev4_motors = [["i", "Flexor Pollicis Brevis", 1],
										["i", "Flexor Pollicis Longus", -1],
										["i", "Abductor Pollicis Brevis", 1],
										["i", "Adductor Pollicis Oblique", -1],
										["i", "Adductor Pollicis Transverse", -1],
										["i", "Opponens Pollicis", 1]]
										
		self.pico_dev5_motors = self.pico_dev3_motors
                              
		self.pico_device = PicoDevice()
		self.pico_devices_addresses = [0x3E, 0x40, 0x42, 0x44, 0x46]
        
	def process_act_data(self, actuators_data):
		rpi_device_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.rpi_motors]
		self.process_rpi_device(rpi_device_data)
		
		pico_dev1_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.pico_dev1_motors]
		pico_dev2_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.pico_dev2_motors]
		pico_dev3_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.pico_dev3_motors]
		pico_dev4_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.pico_dev4_motors]
		pico_dev5_data = [int(actuators_data[digit][name] * m_dir) for digit, name, m_dir in self.pico_dev5_motors]
		
		self.process_pico_device(self.pico_devices_addresses[0], pico_dev1_data)
		self.process_pico_device(self.pico_devices_addresses[1], pico_dev2_data)
		self.process_pico_device(self.pico_devices_addresses[2], pico_dev3_data)
		self.process_pico_device(self.pico_devices_addresses[3], pico_dev4_data)
		self.process_pico_device(self.pico_devices_addresses[4], pico_dev5_data)
		
	def process_rpi_device(self, rpi_actuators_data):
		self.rpi_device.act(rpi_actuators_data)
	
	def process_pico_device(self, address, pico_actuators_data):
		act_data = [act + 1 for act in pico_actuators_data]
		
		print(f"Sending Act Data for Pico @ {address} \n Data: {act_data}")
		self.pico_device.act(address, act_data)

class ActionMsg(BaseModel):
    data: dict

GPIO.setmode(GPIO.BCM)

controller = DARMRPiController()
app = FastAPI()

@app.post("/act/")
async def act(action: ActionMsg):
    # print(f"Data:")
    # pprint.pprint(action.data)
    
    controller.process_act_data(action.data)

    return True
    
@app.websocket("/ws/act")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive action command from the client as JSON
            action = await websocket.receive_json()
            
            # Process the received message
            controller.process_act_data(action["data"])
        except WebSocketDisconnect:
            # Handle disconnection
            break
