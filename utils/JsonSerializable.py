class JsonSerializable:
    @classmethod
    def from_dict(cls, data):
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        if isinstance(data, dict):
            kwargs = {}
            for key, value in data.items():
                sub_class = cls.__annotations__.get(key)
                if isinstance(value, dict) and issubclass(sub_class, JsonSerializable):
                    kwargs[key] = sub_class.from_dict(value)
                else:
                    kwargs[key] = value
            return cls(**kwargs)
        return data