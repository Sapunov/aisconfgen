import os

from .indextypes import get_type
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
            if not index_field.is_sys:
                fields.append(index_type.get_field())
            if index_field.is_facet:
                facets.append(index_type.get_facet())

        return fields, facets

    def _generate_mappings(self):

        mappings = {}

        for index_field in self.fields.values():
            for source_field in index_field.source_fields:
                if source_field.is_onto or source_field.is_sys:
                    continue
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
            self._get_source_mapping_string(source_name, source_mappings) \
                for source_name, source_mappings in mappings.items())

        output = utils.placeholder_template(
            'index.properties',
            index_fields=fields_string,
            facets=facets_string,
            sources=sources_string)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output)

    def _get_source_mapping_string(self, source_name, source_mapping):

        source_template = f'source_{source_name.lower()}.properties'
        try:
            source_default_content = utils.placeholder_template(
                source_template, source_name=source_name)
            source_default_content = source_default_content.strip()
            source_default_content += '\n#\n'
        except FileNotFoundError:
            source_default_content = ''

        output = f'# {source_name}\n#\n'
        output += source_default_content
        output += '\n'.join(source_mapping)

        return output
