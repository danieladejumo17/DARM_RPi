def trinaryToByte(trinary_digits):
	result = 0
	
	for i in range(len(trinary_digits)):
		result = (result*3) + trinary_digits[i]
		
	return result
    
trinary_digits = [2,1,1,1,1]
print(trinaryToByte(trinary_digits))
