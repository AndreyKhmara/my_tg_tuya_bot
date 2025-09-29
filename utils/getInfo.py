import time
def get_device_info(openapi, device_id):
    return openapi.get(f"/v1.0/devices/{device_id}")


def get_device_status(openapi, device_id):
    return openapi.get(f"/v1.0/devices/{device_id}/status")


def post_turn_device(openapi, device_id, command, delay: float = 0.5):
    body = {
        "commands": [{"code": "switch_1",
                      "value": command, }
                     ], }
    openapi.post(f"/v1.0/devices/{device_id}/commands", body)
    time.sleep(delay)
    return get_device_status(openapi, device_id)
