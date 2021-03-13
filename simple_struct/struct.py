"""
   Copyright 2021 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("Structure", "structure")

import typing


class Structure:
    def __init__(self, _dict: typing.Optional[dict] = None):
        self.from_dict(_dict or dict())

    def __setattr__(self, key, value):
        cls = self.__class__.__dict__[key]
        try:
            if issubclass(cls, Structure):
                raise AttributeError(cls.__name__, __class__.__name__)
        except TypeError:
            if value:
                self.__dict__[key] = value
            elif key not in self.__dict__:
                self.__dict__[key] = None

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, dict(self))

    def from_dict(self, d: dict):
        for key, value in self.__class__.__dict__.items():
            if not key.startswith("_"):
                try:
                    if issubclass(value, Structure):
                        if self.__dict__.get(key):
                            self.__dict__[key].__from_dict(d.get(key) or dict())
                        else:
                            self.__dict__[key] = value(d.get(key))
                except TypeError:
                    setattr(self, key, d.get(key) or value)

    def __iter__(self):
        for key, val in self.__dict__.items():
            if isinstance(val, Structure):
                yield key, dict(val)
            else:
                yield key, val


def structure(cls):
    attr_dict = cls.__dict__.copy()
    del attr_dict["__dict__"]
    del attr_dict["__weakref__"]
    sub_cls = type(cls.__name__, (Structure,), attr_dict)
    sub_cls.__qualname__ = cls.__qualname__
    return sub_cls
