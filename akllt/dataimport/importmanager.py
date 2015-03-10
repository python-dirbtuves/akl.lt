import pathlib


class ImportManager(object):
    def __init__(self, root_page, base_dir):
        self.root_page = root_page
        self.base_path = pathlib.Path(base_dir)
        self.importers = []

    def add_importers(self, importers):
        for importer in importers:
            importer.set_up(self.root_page, self.base_path)
            self.importers.append(importer)

    def iterate(self):
        for importer in self.importers:
            for item in importer.iterate_paths():
                yield importer, item

    def get_total(self):
        total = 0
        for importer in self.importers:
            for _ in importer.iterate_paths():
                total += 1
        return total
