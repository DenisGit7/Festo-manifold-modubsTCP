from pymodbus.client import ModbusTcpClient
import asyncio
import time
import json

# outputs: each digital output module have 8 bits,
# each 2 bits it is 1 valve:
# q7 q6 q5 q4 q3 q2 q1 q0
# 0  1  0  1  1  1  1  1
#  v4    v3    v2    v1
# digital inputs: 16 bits module:
# x15 x14 x13 x12 x11 x10 x9 x8 x7 x6 x5 x4 x3 x2 x1 x0
# digital inputs: 8 bits module:
# x7 x6 x5 x4 x3 x2 x1 x0
# analog inputs: analog range 0-4095

inputs = {
    "module1":"0000000000000000",
    "module2":"0000000000000000",
    "module3":"00000000",
    "analog1":0,
    "analog2":0
}
client = ModbusTcpClient('192.168.1.38',port=502)
connection = client.connect()

print("Connected: " + str(connection))
async def run():
  
    print("Connected: " + str(connection))
    
    #write outputs from write.json, conver binary to decimal
    with open('write.json','r') as openfile:
        json_object =json.load(openfile)
    out1 = int("0b"+json_object["output1"], 2)
    out2 = int("0b"+json_object["output2"], 2)
    out3 = int("0b"+json_object["output3"], 2)
    out4 = int("0b"+json_object["output4"], 2)
    client.write_register(40003, out1)
    client.write_register(40004, out2)
    client.write_register(40005, out3)
    client.write_register(40006, out4)
    print("Outputs 1 : ",json_object["output1"] )
    print("Outputs 2 : ",json_object["output2"] )
    print("Outputs 3 : ",json_object["output3"] )
    
    #read input to read.json convert decimal to binary
    # inTest = client.read_holding_registers(45402,10)
    # print(f"\n**************\n  {inTest.registers}")
    
    in1 =  client.read_holding_registers(45395,1)
    in2 =  client.read_holding_registers(45397,1)
    in3 =  client.read_holding_registers(45399,1)
    in4 =  client.read_holding_registers(45402,1)
    in5 =  client.read_holding_registers(45403,1)
  
    inputs["module1"]=bin(in1.registers[0])[2:].zfill(16)
    inputs["module2"]=bin(in2.registers[0])[2:].zfill(16)
    inputs["module3"]=bin(in3.registers[0])[2:].zfill(8)
    inputs["analog1"]=in4.registers
    inputs["analog2"]=in5.registers
    with open("read.json", "w") as outfile:
        json.dump(inputs, outfile)
    print("Inputs 1 : ",inputs["module1"] )
    print("Inputs 2 : ",inputs["module2"] )
    print("Inputs 3 : ",inputs["module3"] )
    print("Analog 1 : ",inputs["analog1"] )
    print("Analog 2 : ",inputs["analog2"] )
    time.sleep(5)

while True:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(run())