select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select home_team
from "five00k"."public"."premier_league_2425_raw"
where home_team is null



      
    ) dbt_internal_test