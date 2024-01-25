def byte_json2dict(byte_str: bytes) -> dict:
    from ast import literal_eval
    return literal_eval(byte_str.decode('utf-8'))