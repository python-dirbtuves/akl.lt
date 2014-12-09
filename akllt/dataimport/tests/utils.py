import pathlib
import pkg_resources


def fixture(path):
    return pathlib.Path(pkg_resources.resource_filename(
        'akllt', 'dataimport/tests/fixtures/%s' % path
    ))
