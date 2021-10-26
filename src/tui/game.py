import socket
import struct
import sys
import datetime
import json
import time
from enum import Enum
from queue import Queue
import logging


start_delimiter = b'\xe2\x94\x90'
end_delimiter = b'\xe2\x94\x94'


class rcon_event(Enum):
    player_death = 6
    request_data = 34
    rcon_ping = 41


class rcon_receive(Enum):
    ping = 1
    command = 2
    request_match = 5
    request_scoreboard = 7


start_read = b'\xe2\x94\x90'
end_read = b'\xe2\x94\x94'


def connect_to_queue(sock, packet_list: Queue):
    """Takes the sock and gets the first 5 packets and returns it"""
    buffer = b''
    while True:
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
                if event_id == rcon_event.rcon_ping.value:
                    send_packet(sock, "1", rcon_receive.ping.value)
                else:
                    if event_id == rcon_event.player_death.value:
                        send_packet(sock, "1", rcon_receive.request_scoreboard.value)
                    packet_list.put(js)


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


def login(ip: str, port: int, password: str):
    """Logs into the server with the matching port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    send_packet(s, password, 0)
    return s

