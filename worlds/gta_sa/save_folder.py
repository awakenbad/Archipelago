import hashlib

LENGTH = 8


def world_folder_name(seed_name, slot_name):
    if not seed_name or not slot_name:
        return None
    digest = hashlib.sha256(f"{seed_name}\x00{slot_name}".encode("utf-8")).hexdigest()
    return digest[:LENGTH]
