# Report

{% for cat_id, cat in data.categories.items() -%}
## {{ cat.title }}
{% for audit_id, audit in cat.audits.items() %}
### {{ audit.title }}
{%- include [audit.audit_template, "audit_result.md"] %}
{% endfor %}
{%- endfor -%}
