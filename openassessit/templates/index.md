#{{ data.requestedUrl|replace('https://', '')|capitalize }} Assessment

__<{{ data.requestedUrl }}>__

<div id="toc">
<!--TOC-->
</div>

{% for cat_id, cat in data.categories.items() -%}
<hr>
# {{ cat.title }}
{{ cat.description }}
{% for audit in cat.sorted_audits %}

{% include [audit.audit_template, "audit_result.md"] %}
<hr>
<br>
{% endfor %}
{% endfor %}
