{% macro test_custom_score_format(model, column_name) %}

{% set column_name = kwargs.get('column_name') %}

select *
from {{ model }}
where "{{ column_name }}" is not null
  and "{{ column_name }}" not regexp '^[0-9]+-[0-9]+$'

{% endmacro %}