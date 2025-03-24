

SELECT
    match_id,
    matchday,
    home_team,
    away_team,
    home_goals,
    away_goals,
    CASE 
        WHEN home_goals > away_goals THEN 'Home Win'
        WHEN home_goals < away_goals THEN 'Away Win'
        ELSE 'Draw'
    END AS match_result
FROM "five00k"."public"."stg_pl_2425"