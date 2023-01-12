from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses import dataclass

@dataclass
class FormData(JsonSchemaMixin):
    daterange: int

