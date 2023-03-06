import json
from typing import Optional

from pydantic import BaseModel

from settings.settings import ORDERS_DATA, ORDER_NAME
from src.controlls.save_loader import SaveLoad


class ProductDO(BaseModel):
    key:str
    line_number: Optional[list[int]]


    def add_to_file(self):
        sl = SaveLoad(ORDERS_DATA)
        orders = sl.load_from_file()
        orders["order_list"].append(
            {"key": self.key,
             "lineNumber": self.line_number})
        sl.save_to_file(orders)
    @staticmethod
    def delete_from_file(baracode):
        sl = SaveLoad(ORDERS_DATA)
        orders = sl.load_from_file()
        new_file = {ORDER_NAME:[]}
        for order in orders[ORDER_NAME]:
            if not order["key"] == baracode:
                new_file[ORDER_NAME].append(order)
        sl.save_to_file(new_file)





