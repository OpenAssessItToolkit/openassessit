##{{ audit.title }}

{% if audit.description %}
{{ audit.description|escape }}
{% endif %}

{{ audit.scoreDisplayMode }} score = {{ audit.score }}

Note: This is the default `audit_result.md` template. Creating a [custom template](https://github.com/OpenAssessItToolkit/openassessit_templates) called `{{ audit.id|replace('-', '_') }}.md` would allow you to expose and iterate over any Lighthouse data.
