from dataclasses import dataclass, asdict
from typing import TypeVar, ClassVar, Any, Dict, Optional, Union

T = TypeVar("T")


class EntityMeta:
    _entity_meta_options: ClassVar[Dict[str, Any]] = {'exclude_none': False}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        options = {'exclude_none': False}
        meta = getattr(cls, 'Meta', None)
        if meta:
            options['exclude_none'] = getattr(meta, 'exclude_none', False)
        cls._entity_meta_options = options

    def to_dict(self, exclude_none: Optional[bool] = None) -> Dict[str, Any]:
        if exclude_none is None:
            exclude_none = self._entity_meta_options.get('exclude_none', False)
        data = asdict(self)
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        else:
            return data

    @classmethod
    def to_domain(cls, obj):
        if obj:
            instance_data = {key: value for key, value in obj.__dict__.items()}
            formatted_data = {}
            for key, value in instance_data.items():
                if not key.startswith('_'):
                    formatted_data[key] = value

            return cls(**formatted_data)
        return None