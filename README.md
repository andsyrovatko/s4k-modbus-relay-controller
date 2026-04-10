# 🛰 S4K Modbus Relay Control

A lightweight, zero-dependency Python utility for controlling [Ethernet/PoE Modbus Relays](https://www.waveshare.com/wiki/Modbus_POE_ETH_Relay) (specifically tested with Waveshare modules).\
Designed for stability in production environments where reliability is key.

---

### 📋 Features
* **Direct Socket Communication:** No heavy libraries like `pymodbus` required.
* **Instance Protection:** Uses `fcntl` file locking to prevent race conditions during concurrent executions.
* **Health Checks:** Integrated `ICMP` ping check before command execution.
* **Configurable:** All parameters (IP, Port, Channels) are stored in an external `.ini` file.
* **Detailed Logging:** Full audit trail of all `ON/OFF/TOGGLE` actions.

---

### 💻 Requirements
| Requirement | Value |
| :--- | :--- |
| **OS** | Linux (Ubuntu, Debian, LMDE, etc.) |
| **Python** | 3.6+ |
| **Permissions** | Write access to log/lock paths |

---

### ⚙️ Configuration (`config.ini`)
| Section | Parameter | Description | Default |
| :--- | :--- | :--- | :--- |
| **`[modbus]`** | `host` | IP address of the relay | `192.168.X.X` |
| **`[modbus]`** | `port` | TCP port (Waveshare: `4196`) | `4196` |
| **`[modbus]`** | `unit` | Modbus Unit ID | `1` |
| **`[modbus]`** | `coil_base` | Channel base num (`0` or `1`) | `1` |
| **`[modbus]`** | `timeout` | Socket timeout (sec) (only view) | `1` |
| **`[modbus]`** | `max_channel`| Max channel index (e.g., `7`). `7` for `coil_base=1` too. | `7` |
| **`[paths]`** | `lock_file` | Path to `.lock` file | `/tmp/modbus.lock` |
| **`[paths]`** | `log_file`  | Path to `.log` file | `/tmp/modbus.log` |

---

### ⚙️ Installation & Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/andsyrovatko/s4k-modbus-relay-controller.git
    cd s4k-modbus-relay-controller
    ```
2. Configure the tool:
Copy the example config and edit it with your device details:
    ```bash
    cp config.ini.example config.ini
    nano config.ini
    ```
3. Set executable permissions:
    ```bash
    chmod +x modbus_controller.py
    ```

---

### 🚀 Usage
0. Use via cli or call from another soft:

    ```bash
    # Get script help/usage info
    python3 modbus_controller.py
    # Output: modbus_controller.py <status|on|off|toggle> <channel>

    # Get channel status
    python3 modbus_controller.py status 8
    # Output: Channel 8 is OFF

    # Turn a specific channel ON or OFF
    python3 modbus_controller.py on 8
    # Output: Channel 8 is turned ON

    # Toggle channel state
    python3 modbus_controller.py toggle 8
    # Output: Channel 8 is turned ON
    ```

---

### ⚠️ Important Note
[**!IMPORTANT**]\
This version currently supports Linux only due to the use of fcntl for process locking. Windows support is planned for future releases.

---

### ⚠️ Disclaimer
> **Use at your own risk!** These scripts are designed for administrative tasks and may perform destructive actions (like killing processes or deleting config files). The author is not responsible for any data loss or system instability. Always test in a sandbox environment first.

---

### ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
