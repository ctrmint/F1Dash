#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------------------------
# Test tool to receive packed values.
# Assumes packed data is of fixed size.
# ----------------------------------------------------------------------------------------------------------------------
import struct
import socket

# Configure listener IP & Port for UDP transmission of packed values
global udp_ip
global udp_port
udp_ip = "0.0.0.0"
udp_port = 20777

global fmt
fmt = '<' + '70' + 'f'  # define structure of packed data

global s
s = struct.Struct(fmt)  # declare structure


def net_rx(UDP_IP, UDP_PORT):
    # Receive packet from wire
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)  # receiving from socket
    return data


def receiver():
    data_gear = 1
    data_mph = 1
    data_mph_fix = 1
    data_brake = 1
    data_rpm = 1
    data_psi = 1
    data_sector = 1
    data_sector1 = 1
    data_sector2 = 1
    data_fuel_in_tank = 1
    data_fuel_capacity = 1
    rx_data = net_rx(udp_ip, udp_port)
    if rx_data:
        unpacked_data = s.unpack(rx_data)                  #  unpack data into tuple, requires correct 'fmt'
        data_mph = unpacked_data[7]
        data_mph_fix = (data_mph * 2.23)
        data_gear = unpacked_data[33]
        data_rpm = unpacked_data[37]

        data_fuel_in_tank = unpacked_data[45]
        data_fuel_capacity = unpacked_data[46]

        data_sector = unpacked_data[48]
        data_sector1 = unpacked_data[49]
        data_sector2 = unpacked_data[50]

        data_brake = unpacked_data[51]
        data_psi = unpacked_data[58]

        data_last_lap = unpacked_data[62]

    return data_gear, data_mph_fix, data_brake, data_rpm, data_psi, data_sector, data_sector1, data_sector2, data_last_lap, data_fuel_in_tank, data_fuel_capacity


def dummy_receiver():
    packet_count = 1
    return packet_count


