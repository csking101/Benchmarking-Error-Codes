import random

def generate_random_binary_string(length: int) -> str:
  #The length is in bits
    binary_string = ''
    for i in range(length):
        bit = random.randint(0, 1)
        binary_string += str(bit)
    return binary_string

import os

PATH = os.path.join(os.path.abspath("./dataset"))

def string_to_binary(s):
    binary_string = ''
    for c in s:
        binary_string += format(ord(c), '08b') # convert to binary and pad to 8 digits
    return binary_string

#import crcmod

def crc_check(data):
    return ''
    crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0xFFFFFFFF, xorOut=0xFFFFFFFF)
    crc = crc32_func(data.encode('utf-8'))
    crc_bytes = crc.to_bytes(4, byteorder='big')
    crc_binary = ''.join(format(byte, '08b') for byte in crc_bytes)
    #return crc_binary
    return ''

def pad_binary(binary_string, n):
    padded_string = binary_string.zfill(n)
    return padded_string

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

#https://www.techtarget.com/searchnetworking/reference/IEEE-802-Wireless-Standards-Fast-Reference

import string

def generate_random_ascii_string(length):
    # Generate a random ASCII string of the given length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def message_gen(message_data: str = "random",#Minimum is 46 bytes,that is length of at least 6 characters
               protocol: str = "802.3",
               sender_address: str = "000000000010001000011001000010100010111101001010",#00:22:19:10:2F:4A
               destination_address: str = "000000000010001000011001101010111000110110010010"):#00:22:19:AB:8D:92

    """This function takes in these parameters and generates the message as per the given payload"""

    if protocol == "802.1d":
      #This is the bridging protocol, used in the spanning tree protocols
      #Using a special unit called the Bridge Protocol Unit
      #https://www.networkplayroom.com/2017/09/bpdu-format-and-stp-timers.html
      #This is a frame that's encapsulated in an ethernet frame itself

      preamble = ''.join([str(i % 2) for i in range(7*8)])
      sfd = '10101011'
      destination_address = '000000011000000011000010000000000000000000000000' #A multicase address
      sender_address = sender_address

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

      frame_contents = [preamble,sfd,destination_address,sender_address,ether_type,stp_header,stp_payload,crc]

    elif protocol == "802.3":
      #This is the Ethernet protocol, assuming sender and receiver both are Dell PCs
      #https://www.geeksforgeeks.org/ethernet-frame-format/
      #Assuming a unicast, Source Address is always an individual address (Unicast), the least significant bit of the first byte is always 0

      preamble = ''.join([str(i % 2) for i in range(7*8)]) #Nowadays, not needed
      sfd = '10101011'
      
      destination_address = destination_address
      sender_address = sender_address

      message_data_length = 46 if len(message_data)*8 < 46 else len(message_data)*8
      length = pad_binary(str(bin((7+1+6+6+2+4)*8+message_data_length)[2:]),2*8)#We just need to add the length of the data later, this will be in bits

      data = string_to_binary(message_data)
      if len(data) < 46:
        data = "".join(['0' for i in range(46-len(data))]) + data
      if len(data) > 1500:
        raise ValueError("The ethernet frame (802.3) can hold 1500 bytes at most")

      crc = crc_check("".join([destination_address,sender_address,length,data]))

      frame_contents = [preamble,sfd,destination_address,sender_address,length,data,crc]

    elif protocol == "802.6":
      #This is for DQDB(Distributed Queue Dual Bus) used in MANs, MAC protocol over bus network

      preamble = ''.join([str(i % 2) for i in range(7*8)])
      sdu = string_to_binary(message_data)
      flag = '01111110'
      crc = crc_check("".join([sdu]))

      frame_contents = [preamble,sdu,flag,crc]

    elif protocol == "802.11":
      #This is for WLANs that uses high frequency radio waves instead of cables for connecting devices
      #https://www.oreilly.com/library/view/80211-wireless-networks/0596100523/ch04.html

      frame_control = "1100000010000000"
      duration = "0000000000000000"
      destination_address = "000000000000101001011110000100100011010001010110"#Sample cisco network device
      source_address = sender_address
      transmitter_address = sender_address #Assuming that the sender itself transmitted the frame
      sequence_control = "0"*16
      receiver_address = "0010100000010010000110000001000000000000000000000000000000000000"#Assuming recevier device and the destination aren't the same
      data = string_to_binary(message_data)

      crc = crc_check("".join([frame_control,duration,receiver_address,source_address,transmitter_address,sequence_control,receiver_address,data]))

      frame_contents = [frame_control,duration,receiver_address,source_address,transmitter_address,sequence_control,receiver_address,data,crc]

    elif protocol == "802.15.4":
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
      data = string_to_binary(message_data)

      crc = crc_check("".join([frame_control,sequence_number,destination_pan_id,destination_address,source_pan_id,source_address,auxiliary_security_header,data]))

      frame_contents = [preamble,sfd,frame_control,sequence_number,destination_pan_id,destination_address,source_pan_id,source_address,auxiliary_security_header,data,crc]

    elif protocol == "802.15.1":
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

      data = string_to_binary(message_data)

      frame_contents = [access_code,headers,data]

    elif protocol == "802.16":
      #Commercialized as Worldwide Interoperability for Microwave Access (WiMAX), it's for wireless broadband technology
      #https://www.tutorialspoint.com/the-802-16-mac-sublayer-frame-structure

      ec = "0"
      type_frame = "000000"
      ci = "0"
      ek = "0"
      connection_id = "0110101011010101"
      header_crc = crc_check("".join([ec,type_frame,ci,ek,connection_id]))
      data = string_to_binary(message_data)

      length = pad_binary(str(bin(52+len(data)*8))[2:],11)

      crc = crc_check("".join([ec,type_frame,ci,ek,length,connection_id,header_crc,data]))

      frame_contents = ["0",ec,type_frame,ci,ek,length,connection_id,header_crc,data,crc]

    return "".join(frame_contents)

import csv

#Csv store: [protocol,total_length,message_content,message itself]
from main import BCHEncode,BCHDecode,RSEncode,RSDecode,Conv213_Encode,Conv213_Decode
from noise_functions import *

import math
import matlab
import matlab.engine
eng = matlab.engine.start_matlab()

def ber(str1: str,str2: str) -> float:
	assert(len(str1) == len(str2))
	total_errors = 0
	for i in range(len(str1)):
		if (str1[i] != str2[i]):
			total_errors += 1
	return total_errors/len(str1)



with open('test.csv','w') as f:
	writer = csv.writer(f)
	writer.writerow(["Protocol","Total Length","Redundant Bits","Bit Error Rate","Code","Noise Function","Noise Parameter","Encoding Time","Decoding Time","Message"])
	for protocol in ["802.1d","802.3","802.6","802.11","802.15.1","802.15.4","802.16"]:
		for length in [i for i in range(20,201,10)]:
			random_msg_content = generate_random_ascii_string(length)
			random_msg_frame = message_gen(random_msg_content)
			total_length = len(random_msg_frame)
			encoded_msg,encoding_time = timing_function(Conv213_Encode)(random_msg_frame)
			redundant_bits = len(encoded_msg) - total_length
			for noise_func in [RayleighFading,RicianFading]:
				noisy_bits = noise_func(encoded_msg)
				decoded_msg,decoding_time = timing_function(Conv213_Decode)(noisy_bits,len(noisy_bits))
				bit_error_rate = ber(random_msg_frame,decoded_msg)
				f.writerow([protocol,total_length,redundant_bits,bit_error_rate,"Convolution",noise_func.__name__,"None",encoding_time,decoding_time,random_msg_frame])


#for protocol in  ["802.1d","802.3","802.6","802.11","802.15.1","802.15.4","802.16"]:
#   os.mkdir(os.path.join(PATH,protocol))