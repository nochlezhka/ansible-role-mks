{% for k, v in env_vars.items() %}
{{ k }}={{ v }}
{% endfor %}

{% for k, v in secret_env_vars.items() %}
{{ k }}='{{ v }}'
{% endfor %}
