import configparser
import socket
import struct
import sys
import datetime
import json
import time
from enum import Enum
from queue import Queue
import threading

SERVER_SETTINGS_FILE = '/root/.config/BoringManRewrite/custom.ini'

start_delimiter = b'\xe2\x94\x90'
end_delimiter = b'\xe2\x94\x94'

class rcon_event(Enum):
    rcon_ping = 41
    

class rcon_receive(Enum):
    ping = 1
    request_match = 5

start_read = b'\xe2\x94\x90' 
end_read = b'\xe2\x94\x94' 

def strip_first_last(string):
    return string[1:-1]


def connect_to_queue(sock, packet_list, needed_packets = 5):
    buffer = b''
    while len(packet_list) < needed_packets:
        buffer += sock.recv(1024)
        while buffer.find(end_delimiter) != -1 and buffer.find(start_delimiter) != -1: 
            start_index = buffer.find(start_delimiter) 
            end_index = buffer.find(end_delimiter) + len(end_delimiter)
            data = buffer[start_index:end_index]
            buffer = buffer[end_index:] 
            if data != b'': 
                data_info = struct.unpack_from('<'+'3s'+'h',data,0) 
                event_data = struct.unpack_from('<'+'3s'+'h'+'h'+str(data_info[1])+'s',data,0) 
                event_id = event_data[2] 
                message_string = event_data[3].decode().strip() 
                message_string = message_string[:-1]
                js = json.loads(message_string)
                packet_list.append(js)
                if event_id == rcon_event.rcon_ping.value:
                    send_packet(sock, "1", rcon_receive.ping.value)
    return packet_list


def send_packet(sock, packetData, packetEnum):
    packet_message = packetData+"\00"
    packet_size = len(bytes(packet_message, 'utf-8'))
    s = struct.Struct('h'+str(packet_size)+'s')
    packet = s.pack(packetEnum,packet_message.encode('utf-8'))
    sock.send(packet)


def send_request(sock, requestID, packetData, packetEnum):
    packet_message = '"' + requestID + '" "' + packetData + '"'
    send_packet(sock, packet_message, packetEnum)


def login(port, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    send_packet(s, password, 0)
    return s



def get_rcon_credentials():
    config = configparser.ConfigParser()        
    config.read(SERVER_SETTINGS_FILE) 
    port = int(strip_first_last(config['Rcon']['rconport']))
    password = strip_first_last(config['Rcon']['rconpassword'])
    return (port, password)

def get_number_of_bots():
    config = configparser.ConfigParser()
    config.read(SERVER_SETTINGS_FILE)
    return int(strip_first_last(config['Server']['Bots']))


def number_of_humans(packet_list):
    """Returns how many human players are on the server.
     -1 if the match type object is not in the list"""
    for packet in packet_list:
         if 'RequestID' in packet and packet['RequestID'] == 'healthcheck':
             return int(packet['Players']) - get_number_of_bots()
    return -1


if __name__ == "__main__":
    s = login(*get_rcon_credentials())
    packet_list = []
    time.sleep(2)
    send_request(s, "healthcheck", "1", rcon_receive.request_match.value)
    packets = connect_to_queue(s, packet_list)
    s.close()
    player_count = number_of_humans(packets)
    print(player_count)
    if player_count == -1:
        print(packets)
    if player_count == 0:
        sys.exit(1)
    else:
        sys.exit(0)
