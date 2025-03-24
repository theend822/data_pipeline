select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      



select *
from "five00k"."public"."premier_league_2425_raw"
where "None" is not null
  and "None" not regexp '^[0-9]+-[0-9]+$'


      
    ) dbt_internal_test