class CollectorField:
    field_type = type

    @classmethod
    def fields(cls) -> list[str]:
        res = []

        for name_attr, type_ in cls.__dict__["__annotations__"].items():
            if type_ is cls.field_type:
                res.append(f"{cls.__dict__[name_attr]}")

        return res
