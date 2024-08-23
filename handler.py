import threading
import resp

SETs = {}
SETsMu = threading.RLock()

HSETs = {}
HSETsMu = threading.RLock()

def ping(args):
    if len(args) == 0:
        return resp.Value(typ="string", str_value="PONG")
    return resp.Value(typ="string", str_value=args[0].bulk)

def set(args):
    if len(args) != 2:
        return resp.Value(typ="error", str_value="ERR wrong number of arguments for 'set' command")

    key, value = args[0].bulk, args[1].bulk

    with SETsMu:  # Changed from SETs_lock
        SETs[key] = value

    return resp.Value(typ="string", str_value="OK")

def get(args):
    if len(args) != 1:
        return resp.Value(typ="error", str_value="ERR wrong number of arguments for 'get' command")

    key = args[0].bulk

    with SETsMu:  # Changed from SETs_lock
        value = SETs.get(key)

    if value is None:
        return resp.Value(typ="null")
    return resp.Value(typ="bulk", bulk=value)

def hset(args):
    if len(args) != 3:
        return resp.Value(typ="error", str_value="ERR wrong number of arguments for 'hset' command")

    hash_name, key, value = args[0].bulk, args[1].bulk, args[2].bulk

    with HSETsMu:  # Changed from HSETs_lock
        if hash_name not in HSETs:
            HSETs[hash_name] = {}
        HSETs[hash_name][key] = value

    return resp.Value(typ="string", str_value="OK")

def hget(args):
    if len(args) != 2:
        return resp.Value(typ="error", str_value="ERR wrong number of arguments for 'hget' command")

    hash_name, key = args[0].bulk, args[1].bulk

    with HSETsMu:  # Changed from HSETs_lock
        value = HSETs.get(hash_name, {}).get(key)

    if value is None:
        return resp.Value(typ="null")
    return resp.Value(typ="bulk", bulk=value)

def hgetall(args):
    if len(args) != 1:
        return resp.Value(typ="error", str_value="ERR wrong number of arguments for 'hgetall' command")

    hash_name = args[0].bulk

    with HSETsMu:  # Changed from HSETs_lock
        hash_map = HSETs.get(hash_name, {})

    array = []
    for k, v in hash_map.items():
        array.append(resp.Value(typ="bulk", bulk=k))
        array.append(resp.Value(typ="bulk", bulk=v))

    return resp.Value(typ="array", array=array)

Handlers = {
    "PING": ping,
    "SET": set,
    "GET": get,
    "HSET": hset,
    "HGET": hget,
    "HGETALL": hgetall
}
