

WITH cleaned AS (
    SELECT
        matchday,
        TRIM(home_team) AS home_team,
        TRIM(away_team) AS away_team,
        -- Split score into home and away goals
        CAST(SPLIT_PART(score, '-', 1) AS INTEGER) AS home_goals,
        CAST(SPLIT_PART(score, '-', 2) AS INTEGER) AS away_goals
    FROM "five00k"."public"."premier_league_2425_raw"
)
SELECT
    matchday,
    home_team,
    away_team,
    home_goals,
    away_goals,
    -- Add a unique match ID
    ROW_NUMBER() OVER (ORDER BY matchday, home_team, away_team) AS match_id
FROM cleaned