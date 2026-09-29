import os
import threading
import requests

STORAGE_BASE = os.environ['INTEGRATION_PROXY_URL'].strip()
if not STORAGE_BASE:
    raise RuntimeError('INTEGRATION_PROXY_URL must be configured for persistent image storage')
STORAGE_URL = STORAGE_BASE.rstrip('/') + '/objstore/api/v1/storage'
storage_key = None
lock = threading.Lock()

def init_storage(force=False):
    global storage_key
    with lock:
        if storage_key and not force:
            return storage_key
        response = requests.post(f'{STORAGE_URL}/init', json={'emergent_key':os.environ['EMERGENT_LLM_KEY']}, timeout=30)
        response.raise_for_status()
        storage_key = response.json()['storage_key']
        return storage_key

def put_object(path, data, content_type):
    response = requests.put(f'{STORAGE_URL}/objects/{path}',headers={'X-Storage-Key':init_storage(),'Content-Type':content_type},data=data,timeout=90)
    response.raise_for_status()
    return response.json()

def get_object(path):
    response = requests.get(f'{STORAGE_URL}/objects/{path}',headers={'X-Storage-Key':init_storage()},timeout=30)
    response.raise_for_status()
    return response.content,response.headers.get('Content-Type','application/octet-stream')