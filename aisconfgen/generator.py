import os

from .indextypes import get_type
from .settings import TEMPLATED_DIR
from aisconfgen import utils


class Generator:

    mapping_template = 'Sources.{source}.Fields.{source_field}.MapTo = {index_field}'

    def __init__(self, fields):

        self.fields = fields

    def generate(self, filename):

        fields, facets = self._generate_fields_and_facets()
        mappings = self._generate_mappings()

        self._generate_config(fields, facets, mappings, filename)

    def _generate_fields_and_facets(self):

        fields = []
        facets = []

        for index_field in self.fields.values():
            index_type = get_type(index_field)
            fields.append(index_type.get_field())
            facets.append(index_type.get_facet())

        return fields, facets

    def _generate_mappings(self):

        mappings = {}

        for index_field in self.fields.values():
            for source_field in index_field.source_fields:
                line = self.mapping_template.format(
                    source=source_field.source,
                    source_field=source_field.source_field_name,
                    index_field=index_field.index_field
                )
                if source_field.source not in mappings:
                    mappings[source_field.source] = []
                mappings[source_field.source].append(line)

        return mappings

    def _generate_config(self, fields, facets, mappings, filename):

        fields_string = '\n\n'.join(fields)
        facets_string = '\n\n'.join(facets)

        sources_string = '\n\n'.join(
            self._get_source_mapping_string(source, source_mappings) \
                for source, source_mappings in mappings.items())

        output = utils.placeholder_file(
            os.path.join(TEMPLATED_DIR, 'index.properties'),
            index_fields=fields_string,
            facets=facets_string,
            sources=sources_string)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output)

    def _get_source_mapping_string(self, source_name, source_mapping):

        output = f'# {source_name}\n#\n'
        output += '\n'.join(source_mapping)

        return output
