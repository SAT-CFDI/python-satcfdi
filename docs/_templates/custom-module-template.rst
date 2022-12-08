{{ name | escape | underline}}

.. automodule:: {{ fullname }}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__


{% if modules %}
.. rubric:: Modules
.. autosummary::
   :toctree:
   :template: custom-module-template.rst
   :recursive:
{% for item in modules %}
{% if item not in (
      'satcfdi.transform.catalog',
      'satcfdi.transform.objectify',
      'satcfdi.transform.schemas',
      'satcfdi.transform.xmlify',
      'satcfdi.transform.xslt'
) %}
   {{ item }}
{% endif %}
{%- endfor %}
{% endif %}