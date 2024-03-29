import re
from .attribute import Attribute
from uc3m_logistics.order_management_exception import OrderManagementException


class ProductIdAttribute(Attribute):
    def validate(self, attr_value):
        """Validate the attribute value"""
        checksum = 0
        code_read = -1
        res = False
        regex_ean13 = re.compile("^[0-9]{13}$")
        valid_ean13_format = regex_ean13.fullmatch(attr_value)
        if valid_ean13_format is None:
            raise OrderManagementException("Invalid EAN13 code string")

        for i, digit in enumerate(reversed(attr_value)):
            try:
                current_digit = int(digit)
            except ValueError as v_e:
                raise OrderManagementException("Invalid EAN13 code string") from v_e
            if i == 0:
                code_read = current_digit
            else:
                checksum += current_digit * 3 if (i % 2 != 0) else current_digit
        control_digit = (10 - (checksum % 10)) % 10
        if (code_read != -1) and (code_read == control_digit):
            res = True
        else:
            raise OrderManagementException("Invalid EAN13 control digit")
        return attr_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, attr_value):
        return self.validate(attr_value)
