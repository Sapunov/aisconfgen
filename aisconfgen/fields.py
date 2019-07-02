from .utils import str_or_none


class SourceField:

    def __init__(
            self, source, source_field_name, field_description,
            is_title, is_facet, field_type, index_field):

        self.source = str_or_none(source)
        self.source_field_name = str_or_none(source_field_name)
        self.field_description = str_or_none(field_description)
        self.is_title = True if is_title != '' else False
        self.is_facet = True if is_facet != '' else False
        self.field_type = str_or_none(field_type)
        self.index_field = str_or_none(index_field)

    def __str__(self):

        fields = []
        for key in self.__dict__:
            fields.append(f'{key}={self.__dict__[key]}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'

    def __repr__(self):

        return self.__str__()


class IndexField:

    def __init__(self, index_field, field_type, is_facet):

        self.index_field = index_field

        if field_type.endswith('[]'):
            self.field_type = field_type.rstrip('[]')
            self.is_array = True
        else:
            self.field_type = field_type
            self.is_array = False

        self.is_facet = is_facet
        self.source_fields = []

        self._added = set()

    def add_source_field(self, source_field):

        self._ensure_right_type(source_field)
        self._ensure_not_duplicate(source_field)
        self._ensure_facet(source_field)

        self.source_fields.append(source_field)

    def _ensure_right_type(self, source_field):

        index_type = self.field_type
        if self.is_array:
            index_type += '[]'

        assert source_field.field_type == index_type, \
            f'Index field type mismatch. {source_field} must be of type {self.field_type}'

    def _ensure_not_duplicate(self, source_field):

        key = source_field.source + source_field.source_field_name
        assert key not in self._added, f'Diplicate key: {key}'
        self._added.add(key)

    def _ensure_facet(self, source_field):
        '''Все поля источника данного поля индекса должны иметь одинаковое значение is_facet.
        Если есть различия, то надо создать несколько полей индекса
        '''
        assert source_field.is_facet == self.is_facet, \
            f'IS_FACET mismatch: {source_field} has is_facet different from {self.is_facet}'

    def __str__(self):

        fields = []
        for key in self.__dict__:
            fields.append(f'{key}={self.__dict__[key]}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'

    def __repr__(self):

        return self.__str__()
