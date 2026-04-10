#!/usr/bin/env python3
# =============================================================================
# Script Name : modbus_controller.py
# Description : Control Modbus coils via TCP (Modbus RTU over TCP).
# Usage       : python3 modbus_controller.py <status|on|off|toggle> <channel>
# Author      : syr4ok (Andrii Syrovatko)
# Version     : 1.0.0-linux
# =============================================================================
import configparser
import os
import socket
import sys
import time
import subprocess
import logging
import fcntl

# Read configuration (variables will be used later in the code)
config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

# Reading variables (with type conversion)
HOST = config.get('modbus', 'host')
PORT = config.getint('modbus', 'port')
UNIT = config.getint('modbus', 'unit')
COIL_BASE = config.getint('modbus', 'coil_base')
TIMEOUT = config.getint('modbus', 'timeout')
MAX_CHANNEL = config.getint('modbus', 'max_channel')

LOCK_FILE = config.get('paths', 'lock_file')
LOG_FILE = config.get('paths', 'log_file')

log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Cannot create log directory {log_dir}: {e}")
        # Use local log file as instead
        LOG_FILE = "modbus_controller.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d at %H:%M:%S"
)

lock_fp = open(LOCK_FILE, "w")
try:
    fcntl.flock(lock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    print("Another instance is already running.")
    sys.exit(1)

def is_host_reachable(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def modbus_crc(data):
    """CALC CRC16 Modbus"""
    crc = 0xFFFF
    for a in data:
        crc ^= a
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc

def build_write_cmd(channel, state):
    cmd = [0] * 8
    cmd[0] = UNIT
    cmd[1] = 0x05  # Write Single Coil
    cmd[2] = 0x00
    cmd[3] = channel
    cmd[4] = 0xFF if state else 0x00
    cmd[5] = 0x00
    crc = modbus_crc(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    return bytearray(cmd)

def build_read_cmd(channel):
    cmd = [0] * 8
    cmd[0] = UNIT
    cmd[1] = 0x01  # Read Coils
    cmd[2] = 0x00
    cmd[3] = channel
    cmd[4] = 0x00
    cmd[5] = 0x01
    crc = modbus_crc(cmd[0:6])
    cmd[6] = crc & 0xFF
    cmd[7] = crc >> 8
    return bytearray(cmd)

def read_status(sock, channel):
    sock.send(build_read_cmd(channel))
    try:
        resp = sock.recv(8)
        if len(resp) >= 4:
            return bool(resp[3] & 0x01)
    except socket.timeout:
        pass
    return None

def write_channel(sock, channel, state):
    sock.send(build_write_cmd(channel, state))
    time.sleep(0.1)

def toggle_channel(sock, channel):
    state = read_status(sock, channel)
    if state is None:
        print(f"Channel {channel + COIL_BASE} did not respond")
        return
    write_channel(sock, channel, not state)

def usage():
    print(f"Usage: {sys.argv[0]} <status|on|off|toggle> <channel>")
    sys.exit(1)

if len(sys.argv) != 3:
    usage()

# Command and channel processing
command_input = sys.argv[1].lower()
channel_input = sys.argv[2]

# Converting ON/OFF into a command
if command_input in ['on', 'off', 'toggle', 'status']:
    command = command_input
else:
    # Attempt to accept "ON"/"OFF" as a command
    if command_input.upper() == 'ON':
        command = 'on'
    elif command_input.upper() == 'OFF':
        command = 'off'
    else:
        usage()

try:
    channel = int(channel_input) - COIL_BASE
except ValueError:
    print("Channel must be an integer")
    sys.exit(1)

if not (0 <= channel <= MAX_CHANNEL):
    print(f"Channel must be between {COIL_BASE} and {COIL_BASE + MAX_CHANNEL}")
    sys.exit(1)

if not is_host_reachable(HOST):
    error_msg = f"Host Modbus ({HOST}) is not reachable (ping failed)"
    print(error_msg)
    logging.error(error_msg)
    sys.exit(1)
try:
    with socket.socket() as s:
        s.settimeout(TIMEOUT)
        s.connect((HOST, PORT))

        if command == "status":
            state = read_status(s, channel)
            if state is None:
                print(f"Channel {channel + COIL_BASE} did not respond")
            else:
                print(f"Channel {channel + COIL_BASE} is {'ON' if state else 'OFF'}")

        elif command == "on":
            state_before = read_status(s, channel)
            if state_before is None:
                print(f"Channel {channel + COIL_BASE} did not respond")
            elif state_before:
                print(f"Channel {channel + COIL_BASE} is already ON, no action taken")
            else:
                write_channel(s, channel, True)
                print(f"Channel {channel + COIL_BASE} is turned ON")
                logging.info(f"ON command sent to channel {channel + COIL_BASE}")
        elif command == "off":
            state_before = read_status(s, channel)
            if state_before is None:
                print(f"Channel {channel + COIL_BASE} did not respond")
            elif not state_before:
                print(f"Channel {channel + COIL_BASE} is already OFF, no action taken")
            else:
                write_channel(s, channel, False)
                print(f"Channel {channel + COIL_BASE} is turned OFF")
                logging.info(f"OFF command sent to channel {channel + COIL_BASE}")
        elif command == "toggle":
            state_before = read_status(s, channel)
            toggle_channel(s, channel)
            if state_before is None:
                print(f"Channel {channel + COIL_BASE} did not respond")
            else:
                print(f"Channel {channel + COIL_BASE} is turned {'OFF' if state_before else 'ON'}")
                logging.info(f"TOGGLE {'-->OFF' if state_before else '-->ON'} command sent to channel {channel + COIL_BASE}")
        else:
            usage()
except (socket.timeout, ConnectionRefusedError, OSError) as e:
    error_msg = f"Connection error to host Modbus ({HOST}:{PORT}) - {e}"
    print(error_msg)
    logging.error(error_msg)
    sys.exit(1)

sys.exit(0)
