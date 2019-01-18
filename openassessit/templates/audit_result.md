## {{ audit.title }}

{% if audit.description %}
{{ audit.description|trim|escape }}
{% endif %}

{% if audit.details %}
__Lighthouse audit contains details__
{% endif %}

{{ audit.scoreDisplayMode|capitalize }} score = {{ audit.score }}

Note: This is the default `audit_result.md` template. Creating a custom template called `{{ audit.id|replace('-', '_') }}.md` would allow you to expose any meta you choose.