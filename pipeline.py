import random

def generate_random_binary_string(length: int) -> str:
  #The length is in bits
    binary_string = ''
    for i in range(length):
        bit = random.randint(0, 1)
        binary_string += str(bit)
    return binary_string

def string_to_binary(s):
    binary_string = ''
    for c in s:
        binary_string += format(ord(c), '08b') # convert to binary and pad to 8 digits
    return binary_string

import crcmod

def crc_check(data):
    crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0xFFFFFFFF, xorOut=0xFFFFFFFF)
    crc = crc32_func(data.encode('utf-8'))
    crc_bytes = crc.to_bytes(4, byteorder='big')
    crc_binary = ''.join(format(byte, '08b') for byte in crc_bytes)
    #return crc_binary
    return ''

def pad_binary(binary_string, n):
    padded_string = binary_string.zfill(n)
    return padded_string

#https://www.techtarget.com/searchnetworking/reference/IEEE-802-Wireless-Standards-Fast-Reference

import string

def generate_random_ascii_string(length):
    # Generate a random ASCII string of the given length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class Frame:
  def __init__(self,
               #data_length: int,
               message_data: str = "random",#Minimum is 46 bytes,that is length of at least 6 characters
               protocol: str = "802.3",
               sender_address: str = "000000000010001000011001000010100010111101001010",#00:22:19:10:2F:4A
               destination_address: str = "000000000010001000011001101010111000110110010010"):#00:22:19:AB:8D:92
    #Addresses are MAC addresses 
    #Dell's MAC Address format: 00:22:19:XX:YY:ZZ
    #Default end users are Dell PCs
    self.protocol = protocol
    #self.data_length = data_length
    self.message_data = message_data
    self.sender_address = sender_address
    self.destination_address = destination_address #This depends on the protocol
    self.frame_contents = []
    self.binary_string = ""

    self.generate_frame()
    self.generate_string()

  def generate_frame(self) -> None:
    if self.protocol == "802.1d":
      #This is the bridging protocol, used in the spanning tree protocols
      #Using a special unit called the Bridge Protocol Unit
      #https://www.networkplayroom.com/2017/09/bpdu-format-and-stp-timers.html
      #This is a frame that's encapsulated in an ethernet frame itself

      preamble = ''.join([str(i % 2) for i in range(7*8)])
      sfd = '10101011'
      destination_address = '000000011000000011000010000000000000000000000000' #A multicase address
      sender_address = self.sender_address

      ether_type = '0000000000000000' #identifies the type of protocol being used, which is usually set to 0x0000 for STP frames
      
      stp_header = ''
      protocol_id = '0000000000000000' 
      version = '00000000'
      bpdu_type  = '00000000'
      flags = '00000000'
      stp_header = protocol_id + version + bpdu_type + flags

      #STP Payload:
         # Protocol Version: 00
         # BPDU Type: 00 (Configuration BPDU)
         # Flags: 00000000
         # Root Identifier: 1000000000000001 0000000000000001 0010001000110011
         # Root Path Cost: 00000000 00000001 01001100 00000000
         # Bridge Identifier: 1000000000000001 0001000100100011 0010001000110100
         # Port Identifier: 1000000000000010
         # Message Age: 00000000 00000000 00000000 00101000 (20 seconds)
         # Max Age: 00000000 00000000 00000000 00100011 (35 seconds)
         # Hello Time: 00000000 00000000 00000000 00000010 (2 seconds)
         # Forward Delay: 00000000 00000000 00000000 00001111 (15 seconds)
         # Topology Change: 00000000

      stp_payload = ''
      root_bridge_priority_number = '0'*16
      root_bridge_mac_address = '100000000000000100000000000000010010001000110011'
      root_path_cost = '00000000000000010100110000000000'
      sender_bridge_priority_number = '0'*16
      sender_bridge_mac_address = '100000000000000100010001001000110010001000110100'
      port_id = '1000000000000010'
      message_age = '0000000000101000'
      maximum_age = '0000000000100011'
      hello_time = '0000000000000010'
      forward_delay = '0000000000001111'

      stp_payload = root_bridge_priority_number + root_bridge_mac_address + root_path_cost + sender_bridge_priority_number + sender_bridge_mac_address + port_id + message_age + maximum_age + hello_time + forward_delay
      
      crc = crc_check("".join([destination_address,sender_address,ether_type,stp_header,stp_payload]))

      self.frame_contents = [preamble,sfd,destination_address,sender_address,ether_type,stp_header,stp_payload,crc]    

    elif self.protocol == "802.3":
      #This is the Ethernet protocol, assuming sender and receiver both are Dell PCs
      #https://www.geeksforgeeks.org/ethernet-frame-format/
      #Assuming a unicast, Source Address is always an individual address (Unicast), the least significant bit of the first byte is always 0

      preamble = ''.join([str(i % 2) for i in range(7*8)]) #Nowadays, not needed
      sfd = '10101011'
      
      destination_address = self.destination_address
      sender_address = self.sender_address

      message_data_length = 46 if len(self.message_data)*8 < 46 else len(self.message_data)*8
      length = pad_binary(str(bin((7+1+6+6+2+4)*8+message_data_length)[2:]),2*8)#We just need to add the length of the data later, this will be in bits

      data = string_to_binary(self.message_data)
      if len(data) < 46:
        data = "".join(['0' for i in range(46-len(data))]) + data
      if len(data) > 1500:
        raise ValueError("The ethernet frame (802.3) can hold 1500 bytes at most")

      crc = crc_check("".join([destination_address,sender_address,length,data]))

      self.frame_contents = [preamble,sfd,destination_address,sender_address,length,data,crc]

    elif self.protocol == "802.6":
      #This is for DQDB(Distributed Queue Dual Bus) used in MANs, MAC protocol over bus network

      preamble = ''.join([str(i % 2) for i in range(7*8)])
      sdu = string_to_binary(self.message_data)
      flag = '01111110'
      crc = crc_check("".join([sdu]))

      self.frame_contents = [preamble,sdu,flag,crc]

    elif self.protocol == "802.11":
      #This is for WLANs that uses high frequency radio waves instead of cables for connecting devices
      #https://www.oreilly.com/library/view/80211-wireless-networks/0596100523/ch04.html

      frame_control = "1100000010000000"
      duration = "0000000000000000"
      destination_address = "000000000000101001011110000100100011010001010110"#Sample cisco network device
      source_address = self.sender_address
      transmitter_address = self.sender_address #Assuming that the sender itself transmitted the frame
      sequence_control = "0"*16
      receiver_address = "0010100000010010000110000001000000000000000000000000000000000000"#Assuming recevier device and the destination aren't the same
      data = string_to_binary(self.message_data)

      crc = crc_check("".join([frame_control,duration,receiver_address,source_address,transmitter_address,sequence_control,receiver_address,data]))

      self.frame_contents = [frame_control,duration,receiver_address,source_address,transmitter_address,sequence_control,receiver_address,data,crc]

    elif self.protocol == "802.15.4":
      #IEEE 802.15.4 is a low-cost, low-data-rate wireless access technology for devices that are operated or work on batteries,that is,low-rate wireless personal area networks (LR-WPANs)
      #https://www.researchgate.net/figure/Data-frame-format-of-IEEE-802154_fig2_47737848
      #We are sending from one device to another on the same personal area network

      preamble = ''.join([str(i % 2) for i in range(7*8)]) #Nowadays, not needed
      sfd = '10101011'

      frame_control = '01000010110000000010000000000000'# Frame Control (0x4240 = data frame, short address mode, no security)
      sequence_number = '00000001'
      destination_pan_id = '0000111100000001'
      destination_address = '0000000000000101' #Short address mode
      source_pan_id = '0000111100000001'
      source_address = '0000000000000110' #Short address mode
      auxiliary_security_header = '' #It's an optional field
      data = string_to_binary(self.message_data)

      crc = crc_check("".join([frame_control,sequence_number,destination_pan_id,destination_address,source_pan_id,source_address,auxiliary_security_header,data]))

      self.frame_contents = [preamble,sfd,frame_control,sequence_number,destination_pan_id,destination_address,source_pan_id,source_address,auxiliary_security_header,data,crc]

    elif self.protocol == "802.15.1":
      #These are bluetooth frames
      #Tannenbaum textbook, chap 4, pg 326,5th ed.
      #https://notes.eddyerburgh.me/computer-networking/bluetooth

      access_code = '101011110110101101000111001111010110001001011010011101110111011'
      
      header = ''
      addr = '101'
      err_type = '0000'
      f = '1'
      a = '1'
      s = '0'
      crc = crc_check("".join([addr,err_type,f,a,s]))
      header = "".join([addr,err_type,f,a,s,crc])
      headers = header*3

      data = string_to_binary(self.message_data)

      self.frame_contents = [access_code,headers,data]

    elif self.protocol == "802.16":
      #Commercialized as Worldwide Interoperability for Microwave Access (WiMAX), it's for wireless broadband technology
      #https://www.tutorialspoint.com/the-802-16-mac-sublayer-frame-structure

      ec = "0"
      type_frame = "000000"
      ci = "0"
      ek = "0"
      connection_id = "0110101011010101"
      header_crc = crc_check("".join([ec,type_frame,ci,ek,connection_id]))
      data = string_to_binary(self.message_data)

      length = pad_binary(str(bin(52+len(data)*8))[2:],11)

      crc = crc_check("".join([ec,type_frame,ci,ek,length,connection_id,header_crc,data]))

      self.frame_contents = ["0",ec,type_frame,ci,ek,length,connection_id,header_crc,data,crc]
      
  def generate_string(self):
    self.binary_string = "".join(self.frame_contents)
    #for item in self.frame_contents:
    #    print(item,len(item))

  def get_string(self):
    return self.binary_string


class MessageBatch:
  def __init__(self,message_length: int = 6,batch_size: int = 32,message_data_array=[],protocol: str = "802.3"):
    #The format specifies what type of frame will be sent across, the default is the frame for ethernet
    self.message_length = message_length
    self.batch_size = batch_size
    self.message_data_array = message_data_array
    self.protocol = protocol
    self.messages = []

    self.generate_batch()

  def generate_batch(self):
    if self.message_data_array != []:
      #If there aren't any custom messages
      for _ in range(self.batch_size):
        self.messages.append(Frame(message_data = generate_random_ascii_string(self.message_length),protocol=self.protocol))
    else:
      #For custom messages
      for message in self.message_data_array:
        self.messages.append(Frame(message_data = message,protocol=self.protocol))

  def __getitem__(self,index):
    return self.messages[index]

  def apply(self,func):
    self.messages = [func(item) for item in self.messages] 

  def apply_with_params(self,func,*args):
    self.messages = [func(item,*args) for item in self.messages]


import time

def timing_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        #print(f"Function {func.__name__!r} executed in {end_time - start_time} seconds")
        time_taken = end_time - start_time

        return (result,time_taken)

    return wrapper

#For each type of error code we'll make a module with it extending the base class:
class ErrorCode:
  def __init__(self):
    pass

  def encode(self,data):
    #Takes binary string and returns the same
    pass

  def decode(self,data):
    #Takes binary string and returns the same
    pass

  def time_encode(self,data):
    timed_encode = timing_function(self.encode)
    return timed_encode(data)

  def time_decode(self,data):
    timed_decode = timing_function(self.decode)
    return timed_decode(data)

class Benchmark():
  def __init__(self,
               code,#We need an instance of the code object
               messages = [],#If the messages are specified then we will not generate messages of random lengths(length of payload)
               lengths = [i for i in range(1,101)],
               protocols = ["802.1d","802.3","802.6","802.11","802.15.1","802.15.4","802.16"],
               noises = [],#Fill this up with an array of functions
               batch_size = 32,
               verbose = False,
               *args
               ):
    #Different messages, different lengths,different protocols(Process as a message batch),different noises,different error codes
    self.messages = messages
    self.lengths = lengths
    self.protocols = protocols
    self.code = code
    self.noises = noises
    self.message_batches = []
    self.noisy_batches = []#It will create a 2d list, where the 1st list corresponds to the first noise function and so on
    self.batch_size = batch_size
    self.verbose = verbose
    self.args = args

    self.generate_message_batches()
    self.encode()
    self.apply_noise_functions()
    self.decode()

  def generate_message_batches(self):
    #Generate message batches of different lengths and protocols

    if len(self.messages) == 0:
      #If there are no custom messages
      for message_length in self.lengths:
        for protocol in self.protocols:
          batch = MessageBatch(message_length = message_length,
                              batch_size = self.batch_size,
                              protocol = protocol)
          
          self.message_batches.append(batch)
    else:
      #There are custom messages
      for protocol in self.protocols:
        batch = MessageBatch(message_data_array = self.messages,
                            protocol = protocol)
        
        self.message_batches.append(batch)

  def encode(self):
    for message_batch in self.message_batches:
      message_batch.apply(self.code.encode,*self.args)

  def apply_noise_functions(self):
    #It will create a 2d list, where the 1st list corresponds to the first noise function and so on
    for noise_function in self.noises:
      temp = []
      for message_batch in self.message_batches:
        temp_msg_batch = message_batch
        temp_msg_batch.apply(noise_function)
        temp.append(temp_msg_batch)
      self.noisy_batches.append(temp)

  def decode(self):
    for noisy_batch_list in self.noisy_batches:
      for noisy_batch in noisy_batch_list:
        noisy_batch.apply(self.code.decode,*self.args)

# -------------------------------
#This is for testing purposes

'''
import matlab.engine
eng = matlab.engine.start_matlab()

class HammingCode(ErrorCode):
    def __init__(self):
        super().__init__()

    def encode(self,data):
        data = matlab.double(data)
        encoded = eng.encode(data,7,4,'hamming/binary')
        encoded = list(encoded)
        return encoded
    
    def decode(self,encoded):
        encoded = matlab.double(encoded)
        decoded = eng.decode(encoded,7,4,'hamming/binary')
        decoded = list(decoded)
        return decoded'''