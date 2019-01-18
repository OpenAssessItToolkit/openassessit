<style>
img { max-width:500px; height: auto; max-height: 500px; min-width:10px; min-height:10px; }
img,iframe {border: 1px solid #ccc;}
a { color: blue; }
pre code { font: 9px; }
pre { font: inherit; word-wrap: break-word; background: none; border: none; }
.force-thumbnail { width: 150px; }
.force-thumbnail img { height: auto; }
</style>

# {{ data.requestedUrl|replace('https://', '')|capitalize }} Assessment

__<{{ data.requestedUrl }}>__


{% for cat_id, cat in data.categories.items() -%}
<hr>
# {{ cat.title }}
{{ cat.description }}
{% for audit in cat.sorted_audits %}

{%- include [audit.audit_template, "audit_result.md"] %}
<hr>
<br>
{% endfor %}
{%- endfor -%}
