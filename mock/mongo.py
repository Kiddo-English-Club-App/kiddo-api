from uuid import uuid4, UUID
import base64

def bson(uuid: str = None) -> dict:
    uuid_obj = uuid4() if not uuid else UUID(uuid)
    base64_uuid = base64.b64encode(uuid_obj.bytes).decode('utf-8')
    return {
        "$binary": {
            "base64": base64_uuid,
            "subType": "04"
        }
    }