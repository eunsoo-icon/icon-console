import re
from typing import Optional

BUILTIN_SCORE_ADDRESS_MAPPER = {
    'governance': f"cx{'0'*39}1",
    'chain': f"cx{'0'*40}",
}
DATA_BYTE_ORDER = 'big'  # big endian
DEFAULT_STEP_LIMIT = 10_000_000
ICX = 10 ** 18


def int_to_bytes(n: int) -> bytes:
    length = byte_length_of_int(n)
    return n.to_bytes(length, byteorder=DATA_BYTE_ORDER, signed=True)


def bytes_to_int(v: bytes) -> int:
    return int.from_bytes(v, byteorder=DATA_BYTE_ORDER, signed=True)


def byte_length_of_int(n: int):
    if n < 0:
        # adds 1 because `bit_length()` always returns a bit length of absolute-value of `n`
        n += 1
    return (n.bit_length() + 8) // 8


def bytes_to_hex(data: Optional[bytes], prefix: str = "0x") -> str:
    if not isinstance(data, bytes):
        return "None"

    return f"{prefix}{data.hex()}"


def is_lowercase_hex_string(value: str) -> bool:
    """Check whether value is hexadecimal format or not

    :param value: text
    :return: True(lowercase hexadecimal) otherwise False
    """

    try:
        result = re.match('[0-9a-f]+', value)
        return len(result.group(0)) == len(value)
    except:
        pass

    return False
