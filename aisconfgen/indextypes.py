class IndexType:

    field_template = ''
    facet_template = 'Facets.{facet_field_name}.IndexField = {field_name}'
    field_array_template = 'Fields.{field_name}.Array = true'

    def __init__(self, index_field):

        self.index_field = index_field

    def get_field(self):

        assert self.field_template, 'Empty field_template'

        field_str = self._get_field_formatted()

        if self.index_field.is_array:
            field_str += '\n' + self.field_array_template.format(
                field_name=self._get_field_name())

        field_str = self._get_comment() + '\n' + field_str

        return field_str

    def get_facet(self):

        return self.facet_template.format(
            field_name=self._get_field_name(), 
            facet_field_name=self._get_facet_field_name())

    def _get_field_name(self):

        return self.index_field.index_field

    def _get_facet_field_name(self):

        return self._get_field_name() + 'Facet'

    def _get_field_formatted(self):
        
        return self.field_template.format(
            field_name=self._get_field_name())

    def _get_comment(self):

        comments = []
        for source_field in self.index_field.source_fields:
            field_source = f'{source_field.source}.{source_field.source_field_name}'
            comment = '# - '
            if self.index_field.is_onto:
                comment += '[Ontology] '
            else:
                comment += f'[{field_source}] '
            comment += source_field.field_description
            comments.append(comment)

        return '\n'.join(comments) + '\n#'


class Fulltext(IndexType):

    field_template = 'Fields.{field_name}.Type = string\n' \
        + 'Fields.{field_name}.IndexType = fulltext'


class Semantic(IndexType):

    field_template = 'Fields.{field_name}.Type = string\n' \
        + 'Fields.{field_name}.IndexType = semantic'


class Date(IndexType):

    field_template = 'Fields.{field_name}.Type = date'


class Integer(IndexType):

    field_template = 'Fields.{field_name}.Type = integer'


class Boolean(IndexType):

    field_template = 'Fields.{field_name}.Type = boolean'


class OntoSemantic(IndexType):

    field_template = 'Fields.{field_name}.Type = string\n' \
        + 'Fields.{field_name}.IndexType = semantic\n' \
        + 'Fields.{field_name}.FillFromOriginalDocument = true\n' \
        + 'Fields.{field_name}.FillFromProperties = {rdf_path}'

    def _get_field_formatted(self):

        return self.field_template.format(
            field_name=self.index_field.index_field,
            rdf_path=self.index_field.source_fields[0].source_field_name)


class Long(IndexType):

    field_template = 'Fields.{field_name}.Type = long'


class Double(IndexType):

    field_template = 'Fields.{field_name}.Type = double'


class SysString(IndexType):

    def get_field(self):

        raise NotImplementedError()

    def _get_facet_field_name(self):

        name = super()._get_facet_field_name()
        if name.startswith('__'):
            name = name.lstrip('_')
        return name[0].upper() + name[1:]


MAPPING = {
    'fulltext': Fulltext,
    'semantic': Semantic,
    'date': Date,
    'integer': Integer,
    'boolean': Boolean,
    'onto:semantic': OntoSemantic,
    'long': Long,
    'double': Double,
    'sys': SysString
}


def get_type(index_field):

    type_name = index_field.field_type

    if index_field.is_onto:
        type_name = 'onto:' + type_name
    elif index_field.is_sys:
        type_name = 'sys'

    assert type_name in MAPPING, f'Unknown type_name {type_name} in {index_field}'

    return MAPPING[type_name](index_field)
