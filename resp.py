import struct

class Value:
    def __init__(self, typ, str_value=None, num=None, bulk=None, array=None):
        self.typ = typ
        self.str = str_value
        self.num = num
        self.bulk = bulk
        self.array = array

def read(data):
    if data[0] == ord('*'):
        return read_array(data[1:])
    elif data[0] == ord('$'):
        return read_bulk(data[1:])
    elif data[0] == ord('+'):
        return read_simple_string(data[1:])
    elif data[0] == ord(':'):
        return read_integer(data[1:])
    elif data[0] == ord('-'):
        return read_error(data[1:])
    else:
        raise ValueError(f"Unknown type: {chr(data[0])}")

def read_array(data):
    length, data = read_integer(data)
    array = []
    for _ in range(length):
        value, data = read(data)
        array.append(value)
    return Value(typ="array", array=array), data

def read_bulk(data):
    length, data = read_integer(data)
    if length == -1:
        return Value(typ="null"), data
    bulk = data[:length]
    return Value(typ="bulk", bulk=bulk.decode()), data[length+2:]

def read_simple_string(data):
    end = data.index(b'\r\n')
    return Value(typ="string", str_value=data[:end].decode()), data[end+2:]

def read_integer(data):
    end = data.index(b'\r\n')
    return int(data[:end]), data[end+2:]

def read_error(data):
    end = data.index(b'\r\n')
    return Value(typ="error", str_value=data[:end].decode()), data[end+2:]

def marshal(value):
    if value.typ == "array":
        return marshal_array(value)
    elif value.typ == "bulk":
        return marshal_bulk(value)
    elif value.typ == "string":
        return marshal_string(value)
    elif value.typ == "null":
        return marshal_null(value)
    elif value.typ == "error":
        return marshal_error(value)
    elif value.typ == "integer":
        return marshal_integer(value)
    else:
        return b""

def marshal_array(value):
    data = b'*' + str(len(value.array)).encode() + b'\r\n'
    for v in value.array:
        data += marshal(v)
    return data

def marshal_bulk(value):
    return b'$' + str(len(value.bulk)).encode() + b'\r\n' + value.bulk.encode() + b'\r\n'

def marshal_string(value):
    return b'+' + value.str.encode() + b'\r\n'

def marshal_null(value):
    return b'$-1\r\n'

def marshal_error(value):
    return b'-' + value.str.encode() + b'\r\n'

def marshal_integer(value):
    return b':' + str(value.num).encode() + b'\r\n'

def unmarshal(data):
    value, _ = read(data)
    return value

# Rest of resp.py remains the same
