from typing import Any, Dict
import json
from spacy.tokens import Span

class SpacySpanEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Span): return str(obj)
        return json.JSONEncoder.default(self, obj)

def read_message_data(message: Dict) -> Dict:
    return json.loads(message['data'].decode())

def serialize_message_data(data: Any) -> str:
    return json.dumps(data, cls=SpacySpanEncoder)