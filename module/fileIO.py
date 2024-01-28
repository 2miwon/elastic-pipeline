def byte_json2dict(byte: bytes) -> dict:
    import json
    json_string = byte.decode('utf-8').strip()
    data = json.loads(json_string)

def download_file(url: str, directory: str, filename: str):
    import requests
    import os
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
    else:
        raise(f"Failed to download file from {url}")
    
def file_exist(path: str):
    import os
    return os.path.exists(path)