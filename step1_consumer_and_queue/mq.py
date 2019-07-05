from typing import Any, Dict
import json

def read_message_data(message: Dict) -> Dict:
    return json.loads(message['data'].decode())

def serialize_message_data(data: Any) -> str:
    return json.dumps(data)