from enum import Enum

class ControllerType(Enum):
    CACC = "CACC"

    @staticmethod
    def from_string(s):
        for member in ControllerType:
            if member.value == s:
                return member
        raise ValueError(f"No ControllerType member with value '{s}' found")