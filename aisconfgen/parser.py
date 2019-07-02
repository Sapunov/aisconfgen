import csv

from .fields import SourceField, IndexField


HEADERS = [
    'Source', 'SourceFieldName', 'FieldDescription',
    'Title', 'Facet', 'Type', 'IndexField']

SKIP_PREFIXES = ['todo:']


class Parser:

    def __init__(self, filename):

        self.filename = filename
        self.fields = {}

        self._last_source = None

    def parse(self):

        with open(self.filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)

            assert headers == HEADERS, 'Incorrect headers'

            for row in reader:
                assert len(row) == len(HEADERS), \
                    'Number of fields in row is {len(row)} instead of {len(HEADERS)}'

                source_field = self._process_row(row)

                if source_field is None:
                    continue

                if source_field.index_field not in self.fields:
                    self.fields[source_field.index_field] = IndexField(
                        source_field.index_field,
                        source_field.field_type,
                        source_field.is_facet)

                self.fields[source_field.index_field].add_source_field(source_field)

        return self.fields

    def _process_row(self, row):

        if all(col == '' for col in row):
            return None

        source_field = SourceField(*row)

        for skip_prefix in SKIP_PREFIXES:
            if source_field.source_field_name.lower().startswith(skip_prefix):
                return None

        if source_field.source is None:
            source_field.source = self._last_source
        else:
            self._last_source = source_field.source

        return source_field
