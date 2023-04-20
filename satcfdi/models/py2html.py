# -*- coding: utf-8 -*-
"""
HTML Converter
"""
from collections.abc import Mapping, Sequence
from html import escape as html_escape


def dumps(obj, clubbing=True, escape=True, translate_keys=None, default=str):
    """
        Convert object to HTML Table format
    """
    encoder = PY2HTMLEncoder(clubbing, escape, translate_keys, default)
    return "".join(encoder.encode(obj))


def _get_column_headers(py_input):
    """
        This method is required to implement clubbing.
        It tries to come up with column headers for your input
    """
    if py_input and isinstance(py_input, Sequence):
        if isinstance(py_input[0], Mapping):
            # use a dict to maintain consisten order
            return {k: None for r in py_input for k in r.keys()}

    return None


class PY2HTMLEncoder:
    def __init__(self, clubbing=True, escape=True, translate_keys=None, default=str):
        self.clubbing = clubbing
        self.escape = escape
        self.translate_keys = translate_keys
        self.default = default

    def encode(self, input):
        """
            Dispatch JSON input according to the outermost type and process it
            to generate the super awesome HTML format.
            We try to adhere to duck typing such that users can just pass all kinds
            of funky objects to py2html that *behave* like dicts and lists and other
            basic JSON types.
        """
        if isinstance(input, str):
            if self.escape:
                yield html_escape(input)
                return
            else:
                yield input
                return
        if isinstance(input, Mapping):
            yield from self.convert_object(input)
            return

        if isinstance(input, Sequence):
            yield from self.convert_list(input)
            return

        if self.escape:
            yield html_escape(str(self.default(input)))
            return
        else:
            yield str(self.default(input))
            return

    def convert_list(self, list_input):
        """
            Iterate over the JSON list and process it
            to generate either an HTML table or a HTML list, depending on what's inside.
            If suppose some key has array of objects and all the keys are same,
            instead of creating a new row for each such entry,
            club such values, thus it makes more sense and more readable table.

            @example:
                pyObject = {
                    "sampleData": [
                        {"a":1, "b":2, "c":3},
                        {"a":5, "b":6, "c":7}
                    ]
                }
                OUTPUT:
                _____________________________
                |               |   |   |   |
                |               | a | c | b |
                |   sampleData  |---|---|---|
                |               | 1 | 3 | 2 |
                |               | 5 | 7 | 6 |
                -----------------------------

            @contributed by: @muellermichel
        """
        if not list_input:
            return

        if self.clubbing:
            column_headers = _get_column_headers(list_input)

            if column_headers is not None:
                yield "<table>"
                yield '<thead>'
                yield '<tr><th>' + '</th><th>'.join(self.translate_keys(k) for k in column_headers) + '</th></tr>'
                yield '</thead><tbody>'
                for list_entry in list_input:
                    yield '<tr>'
                    for column_header in column_headers:
                        yield "<td>"
                        yield from self.encode(list_entry.get(column_header, ""))
                        yield '</td>'
                    yield '</tr>'
                yield '</tbody></table>'
                return

        # so you don't want or need clubbing eh? This makes @muellermichel very sad... ;(
        # alright, let's fall back to a basic list here...
        yield '<ul>'
        for child in list_input:
            yield "<li>"
            yield from self.encode(child)
            yield "</li>"
        yield '</ul>'

    def convert_object(self, dict_input):
        """
            Iterate over the JSON object and process it
            to generate the super awesome HTML Table format
        """
        if not dict_input:
            return

        yield "<table>"
        for k, v in dict_input.items():
            if v is not None:
                yield "<tr><td class='htd'>"
                yield from self.encode(self.translate_keys(k) + ":")
                yield "</td><td>"
                yield from self.encode(v)
                yield "</td></tr>"
        yield '</table>'
