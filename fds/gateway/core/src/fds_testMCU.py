import serial

def main():
 data = {'type':'mcu'}
 ser = serial.Serial('/dev/ttyACM0', timeout=1)  # open serial port
 ser.write(b'l') 
 try:
  line = ser.readline()
  print line
 except TimeoutError:
  print 'Serial Read Timeout error.'
  ser.close()
  return None
 except: 
  print 'Serial Read unpredicted error.'
  return None
  
 ser.close()
 try:
  mcu_data = dict( ast.literal_eval(line) )
 except:
  print 'MCU message parsing error.' 
  return None
 print mcu_data


if __name__== "__main__":
 main()





