# 🛰 S4K Modbus Relay Control

A lightweight, zero-dependency Python utility for controlling [Ethernet/PoE Modbus Relays](https://www.waveshare.com/wiki/Modbus_POE_ETH_Relay) (specifically tested with Waveshare modules).\
Designed for stability in production environments where reliability is key.

---

### 📋 Features
* **Direct Socket Communication:** No heavy libraries like `pymodbus` required.
* **Cross-Platform:** Full support for `Linux` and `Windows`.
* **Health Checks:** Integrated `ICMP` ping check before command execution.
* **Configurable:** All parameters (IP, Port, Channels) are stored in an external `.ini` file.
* **Smart Paths:** Uses `pathlib` for automatic directory creation (e.g., `logs/` folder).
* **Detailed Logging:** Full audit trail of all `ON/OFF/TOGGLE` actions.

---

### 💻 Requirements
| Requirement | Value |
| :--- | :--- |
| **OS** | Linux, Windows, FreeBSD |
| **Python** | 3.6+ (standard library only) |

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
| **`[paths]`** | `lock_file` | Path to `.lock` file | `modbus.lock` |
| **`[paths]`** | `log_file`  | Path to `.log` file  | `logs/modbus.log` |

**Tip**: It's better to specify relative names in default path values,
so that they work "out of the box" everywhere:

---

### ⚙️ Installation & Portability
The tool is fully portable and can be run directly from a USB drive or any local folder without system-wide installation.
1. Clone the repository:
    ```bash
    git clone https://github.com/andsyrovatko/s4k-modbus-relay-controller.git
    cd s4k-modbus-relay-controller
    ```
2. Configure the tool:
Copy the example config and edit it (the script will automatically find it in its own directory):
* `Linux:`
    ```bash
    cp config.ini.example config.ini && nano config.ini
    ```
* `Windows:`
    ```bash
    copy config.ini.example config.ini
    ```
    (then edit with any text editor)
3. Permissions (`Linux only`):
    ```bash
    chmod +x modbus_controller.py
    ```
    (to start script as `./modbus_controller.py` not `python modbus_controller.py`)
---

### 🚀 Usage
The script supports both Windows and Linux syntax. You can run it from any location by specifying the full path.

| Action | Linux | Windows (CMD/PowerShell) | Result |
| :--- | :--- | :--- | :--- |
| **Get Status** | `./modbus_controller.py status 1` | `python modbus_controller.py status 1` | Channel 1 is OFF |
| **Turn ON** | `./modbus_controller.py on 1` | `python modbus_controller.py on 1` | Channel 1 is turned ON |
| **Turn OFF** | `./modbus_controller.py off 1` | `python modbus_controller.py off 1` | Channel 1 is turned OFF |
| **Toggle** | `./modbus_controller.py toggle 1` | `python modbus_controller.py toggle 1` | Channel 1 is turned OFF (if was ON) |

### 📦 Portable Example (Windows)
Run the script directly from your USB drive (e.g. `F:\`) by specifying the full path:
```powershell
python F:\ModBus\modbus_controller.py status 1
```

---

### [✓] Verified: Tested on Linux (LMDE 7) and Windows 11.

---

### ⚠️ Disclaimer
> **Use at your own risk!** These scripts are designed for administrative tasks and may perform destructive actions (like killing processes or deleting config files). The author is not responsible for any data loss or system instability. Always test in a sandbox environment first.

---

### ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
