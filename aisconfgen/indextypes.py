class IndexType:

    field_template = ''
    facet_template = 'Facets.{field_name}Facet.IndexField = {field_name}'
    field_array_template = 'Fields.{field_name}.Array = true'

    def __init__(self, index_field):

        self.index_field = index_field

    def get_field(self):

        assert self.field_template, 'Empty field_template'

        field_str = self.field_template.format(
            field_name=self.index_field.index_field)

        if self.index_field.is_array:
            field_str += '\n' + self.field_array_template.format(
                field_name=self.index_field.index_field)

        field_str = self._get_comment() + '\n' + field_str

        return field_str

    def get_facet(self):

        return self.facet_template.format(field_name=self.index_field.index_field)


    def _get_comment(self):

        comments = []
        for source_field in self.index_field.source_fields:
            comment = f'# - [{source_field.source}.{source_field.source_field_name}] ' \
                + f'{source_field.field_description}'
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



MAPPING = {
    'fulltext': Fulltext,
    'semantic': Semantic,
    'date': Date,
    'integer': Integer,
    'boolean': Boolean
}


def get_type(index_field):

    type_name = index_field.field_type

    assert type_name in MAPPING, f'Unknown type_name {type_name} in {index_field}'

    return MAPPING[type_name](index_field)
