{{ audit.helpText }}

Score: {{ audit.score }}
{%- if audit.score %}
Display value: {{ audit.displayValue|trim }}
{% endif -%}
