# Taken from:
# https://github.com/ProgrammersOfVilnius/zope-export-tools/blob/master/z2loader.py

import codecs
import configparser
import pathlib


class Z2LoaderError(Exception):
    pass


def unescape(value):
    """Decode b'\xc5\xbe' to 'ž'"""
    assert isinstance(value, str)
    return codecs.escape_decode(value.encode())[0].decode()


# pylint: disable=redefined-builtin,eval-used
def parse_value(filename, key, value):
    name, type = key.split(':')

    if type == 'boolean':
        if value in ('True', 'False'):
            value = (value == 'True')
        else:
            value = int(value)
    elif type == 'int':
        value = int(value)
    elif type in ('string', 'text', 'ustring'):
        pass
    elif type in {'multiple selection', 'tokens'}:
        value = eval(unescape(value))
    else:
        raise Z2LoaderError('%s: unsupported type: %s' % (filename, type))

    return name, value


def parse_properties(filename, items):
    properties = {}
    for key, value in items:
        if ':' not in key:
            raise Z2LoaderError('%s: bad metadata key: %s' % (filename, key))
        value = unescape(value)
        value = value.replace('&nbsp;', ' ')
        name, value = parse_value(filename, key, value)
        properties[name] = value
    return properties


def load_metadata(filename):
    path = pathlib.Path(filename)
    assert path.exists()
    config = configparser.RawConfigParser(delimiters=('=',))
    config.read(str(path))
    properties = config['properties']
    return parse_properties(filename, properties.items())
