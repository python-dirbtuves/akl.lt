# Taken from:
# https://github.com/ProgrammersOfVilnius/zope-export-tools/blob/master/z2loader.py

import pathlib


class Z2LoaderError(Exception):
    pass


def skip_to_properties(lines):
    for line in lines:
        line = line.rstrip('\n')
        if line == '[properties]':
            break


def parse_value(filename, key, value):
    name, type = key.split(':')

    if type == 'boolean':
        if value in ('True', 'False'):
            value = (value == 'True')
        else:
            value = int(value)
    elif type == 'int':
        value = int(value)
    elif type == 'string':
        pass
    elif type == 'text':
        value = value.decode('UTF-8')
    elif type == 'ustring':
        value = unicode(value, 'UTF-8')
    else:
        raise Z2LoaderError('%s: unsupported type: %s' % (filename, type))

    return name, value


def parse_properties(filename, lines):
    properties = {}
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('['):
            break
        if line.startswith('#'):
            continue
        if not line.strip():
            continue
        if ' = ' not in line:
            raise Z2LoaderError('%s: bad metadata line: %s' % (filename, line))
        key, value = line.split(' = ', 1)
        if ':' not in key:
            raise Z2LoaderError('%s: bad metadata key: %s' % (filename, key))
        value = value.decode('string-escape')
        name, value = parse_value(filename, key, value)
        properties[name] = value
    return properties


def load_metadata(filename):
    path = pathlib.Path(filename)
    assert path.exists()
    with path.open('r') as f:
        skip_to_properties(f)
        return parse_properties(filename, f)
