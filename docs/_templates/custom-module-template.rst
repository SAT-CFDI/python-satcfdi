{{ name | escape | underline}}

.. automodule:: {{ fullname }}

   {% if attributes %}
   .. rubric:: Module Attributes
   .. autosummary::
      :toctree:
   {% for item in attributes %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if functions %}
   .. rubric:: Functions
   .. autosummary::
      :toctree:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if classes %}
   .. rubric:: Classes
   .. autosummary::
      :toctree:
      :template: custom-class-template.rst
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}

   {% if exceptions %}
   .. rubric:: Exceptions
   .. autosummary::
      :toctree:
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}

{% if modules %}
.. rubric:: Modules
.. autosummary::
   :toctree:
   :template: custom-module-template.rst
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}