from dataclasses import dataclass, asdict
from typing import Union, get_type_hints
from enum import Enum
import json

class JsonSerializable:
    @classmethod
    def from_dict(cls, data):
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        if isinstance(data, dict):
            kwargs = {}
            for key, value in data.items():
                sub_class = get_type_hints(cls).get(key)
                if sub_class and isinstance(sub_class, type):
                    if issubclass(sub_class, Enum):
                        kwargs[key] = sub_class(value)
                    elif isinstance(value, dict) and issubclass(sub_class, JsonSerializable):
                        kwargs[key] = sub_class.from_dict(value)
                    else:
                        kwargs[key] = value
                else:
                    kwargs[key] = value
            return cls(**kwargs)
        return data
    
    def to_dict(self):
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, JsonSerializable):
                result[key] = value.to_dict()
            elif isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value
        return result

    def to_json(self):
        return json.dumps(self.to_dict())