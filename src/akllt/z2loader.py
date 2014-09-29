# Taken from:
# https://github.com/ProgrammersOfVilnius/zope-export-tools/blob/master/z2loader.py

import os.path


def load_metadata(filename):  # noqa
    meta = {}
    assert os.path.exists(filename)
    f = file(filename, 'r')
    for line in f:
        line = line.rstrip('\n')
        if line == '[properties]':
            break
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('['):
            break
        if line.startswith('#'):
            continue
        if not line.strip():
            continue
        if ' = ' not in line:
            print "%s: bad metadata line: %s" % (filename, line)
            continue
        key, value = line.split(' = ', 1)
        if ':' not in key:
            print "%s: bad metadata key: %s" % (filename, key)
            continue
        name, type = key.split(':')
        value = value.decode('string-escape')
        # TODO: saner type conversion

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
            print "%s: unsupported type: %s" % (filename, type)
            continue

        meta[name] = value
    f.close()

    return meta
