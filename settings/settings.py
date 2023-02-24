import os


def get_serial() -> str:
    # Extract serial from cpuinfo file
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR000000000"
    finally:
        return cpu_serial


SETTINGS_PATH: str = os.getenv("SETTINGS_PATH", "../settings/settings.json")
DATA_FOR_GUI: str = os.getenv("DATA_FOR_GUI", "../src/res/data/data.json")
LOAD_GUI: str = os.getenv("LOAD_GUI", "../src/res/data/gui.json")
ORDERS_DATA: str = os.getenv("ORDERS_DATA", "res/data/order.json")
GUI_NAME: str = os.getenv("GUI_NAME", "elements")
GUI_UPDT: str = os.getenv("GUI_UPDT", "res/presets/")
REQUEST_SETTINGS: str = os.getenv("REQUEST_SETTINGS", "")
REQUEST_WIFI: str = os.getenv("REQUEST_WIFI", "")
REQUEST_GUI: str = os.getenv("REQUEST_GUI", "")
REQUEST_ORDERS: str = os.getenv("REQUEST_ORDERS", "")

ID_RASPI: str = get_serial()
