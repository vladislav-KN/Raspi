import os
from screeninfo import get_monitors
from dotenv import load_dotenv

load_dotenv()


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


def get_number_of_elem() -> int:
    for m in get_monitors():
        if m.is_primary or m.name == "default":
            return m.width // 250 - 1
    return 0


SETTINGS_PATH: str = os.getenv("SETTINGS_PATH", "/settings/settings.json")
DATA_FOR_GUI: str = os.getenv("DATA_FOR_GUI", "/src/res/data/data.json")
LOAD_GUI: str = os.getenv("LOAD_GUI", "/src/res/data/gui.json")
ORDERS_DATA: str = os.getenv("ORDERS_DATA", "/src/res/data/order.json")

CHECK_CONNECTION: str = os.getenv("CHECK_CONNECTION", "https://google.com")
GUI_NAME: str = os.getenv("GUI_NAME", "elements")
GUI_UPDT: str = os.getenv("GUI_UPDT", "/src/res/presets/gui_updt_settings.json")
ORDER_UPDT: str = os.getenv("ORDER_UPDT", "/src/res/presets/order_updt_settings.json")
SETTINGS_UPDT: str = os.getenv("SETTINGS_UPDT", "/src/res/presets/settings_updt_settings.json")

REQUEST_SETTINGS: str = os.getenv("REQUEST_SETTINGS", "")
REQUEST_WIFI: str = os.getenv("REQUEST_WIFI", "")
REQUEST_GUI: str = os.getenv("REQUEST_GUI", "")
REQUEST_ORDERS: str = os.getenv("REQUEST_ORDERS", "")

ID_RASPI: str = get_serial()
NUM_ELEM: int = get_number_of_elem()
