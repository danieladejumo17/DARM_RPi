import smbus
from time import sleep

channel = 1
address = 0x3E

bus = smbus.SMBus(channel)

# data = [2,1,1,1,1]

def trinaryToByte(trinary_digits):
	result = 0
	
	for i in range(len(trinary_digits)):
		result = (result*3) + trinary_digits[i]
		
	return result

while True:
	data_str = input("Input command to Pico: ")
	data = list(map(int, data_str.split(',')))
	byte_data = trinaryToByte(data)
	
	sleep(1)
	try:
		print ("Writing data "+str(byte_data))
		# Write out I2C command: address, cmd, msg[0]
		bus.write_i2c_block_data(address, 0, [byte_data])
	except Exception as e:
		print ("Writing Error "+str(e))
		continue
	
