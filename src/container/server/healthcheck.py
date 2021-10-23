import socket
import struct
import sys
import datetime
import json
import time
from enum import Enum
from queue import Queue
import logging

import toml

from SettingsModel import FullSettings

SERVER_SETTINGS_FILE = '/root/.config/BoringManRewrite/custom{}.ini'

start_delimiter = b'\xe2\x94\x90'
end_delimiter = b'\xe2\x94\x94'

def configure_logging():
    logging.basicConfig(filename='healtcheck.log', level=logging.DEBUG)
    logging.info('Started')

configure_logging()

class rcon_event(Enum):
    rcon_ping = 41


class rcon_receive(Enum):
    ping = 1
    command = 2
    request_match = 5


start_read = b'\xe2\x94\x90'
end_read = b'\xe2\x94\x94'


def strip_first_last(string):
    return string[1:-1]


def connect_to_queue(sock, packet_list = [], needed_packets=5):
    """Takes the sock and gets the first 5 packets and returns it"""
    buffer = b''
    while len(packet_list) < needed_packets:
        buffer += sock.recv(1024)
        while buffer.find(end_delimiter) != -1 and buffer.find(start_delimiter) != -1:
            start_index = buffer.find(start_delimiter)
            end_index = buffer.find(end_delimiter) + len(end_delimiter)
            data = buffer[start_index:end_index]
            buffer = buffer[end_index:]
            if data != b'':
                data_info = struct.unpack_from('<'+'3s'+'h', data, 0)
                event_data = struct.unpack_from(
                    '<'+'3s'+'h'+'h'+str(data_info[1])+'s', data, 0)
                event_id = event_data[2]
                message_string = event_data[3].decode().strip()
                message_string = message_string[:-1]
                js = json.loads(message_string)
                packet_list.append(js)
                if event_id == rcon_event.rcon_ping.value:
                    send_packet(sock, "1", rcon_receive.ping.value)
    return packet_list


def send_packet(sock, packetData, packetEnum):
    """Send the packet to the server"""
    packet_message = packetData+"\00"
    packet_size = len(bytes(packet_message, 'utf-8'))
    s = struct.Struct('h'+str(packet_size)+'s')
    packet = s.pack(packetEnum, packet_message.encode('utf-8'))
    sock.send(packet)


def send_request(sock, requestID, packetData, packetEnum):
    """Send request to the server"""
    packet_message = '"' + requestID + '" "' + packetData + '"'
    send_packet(sock, packet_message, packetEnum)


def login(port: int, password: str):
    """Logs into the server with the matching port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', port))
    send_packet(s, password, 0)
    return s


def current_server_usage(packet_list):
    """Returns how many human players are on the server.
     -1 if the match type object is not in the list"""
    for packet in packet_list:
        if 'RequestID' in packet and packet['RequestID'] == 'healthcheck':
            return int(packet['Players'])
    return -1



def rawsay(socket, message):
    send_packet(socket, 
        'rawsay "{}" "{}"'.format(message, 65280),
        rcon_receive.command.value
    )

def health_check(server_settings: FullSettings):
    """Returns if the server has players in it. False if the server isn't running or it is empty"""
    s = None
    try:
        s = login(int(server_settings.Rcon.RconPort), server_settings.Rcon.RconPassword)
    except socket.error as e:
        return False
    
    # Sleep for 2 seconds because RCON can't handle rapid fire commands
    time.sleep(2)
    send_request(s, "healthcheck", "1", rcon_receive.request_match.value)
    time.sleep(2)
    packets = connect_to_queue(s)
    logging.debug(str(packets))
    logging.debug("Total Players: " + str(current_server_usage(packets)))
    rawsay(s, current_server_usage(packets))
    s.close()
    curr_usage = current_server_usage(packets)
    if curr_usage < 0 or (curr_usage - int(server_settings.Server.Bots) > 0):
        return True
    else:
        return False
