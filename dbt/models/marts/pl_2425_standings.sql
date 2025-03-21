{{ config(materialized='table') }}

WITH match_points AS (
    SELECT
        home_team AS team,
        SUM(CASE 
            WHEN home_goals > away_goals THEN 3
            WHEN home_goals = away_goals THEN 1
            ELSE 0
        END) AS points,
        COUNT(*) AS matches_played,
        SUM(CASE WHEN home_goals > away_goals THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN home_goals = away_goals THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN home_goals < away_goals THEN 1 ELSE 0 END) AS losses,
        SUM(home_goals) AS goals_for,
        SUM(away_goals) AS goals_against
    FROM {{ ref('stg_pl_2425') }}
    GROUP BY home_team

    UNION ALL

    SELECT
        away_team AS team,
        SUM(CASE 
            WHEN away_goals > home_goals THEN 3
            WHEN away_goals = home_goals THEN 1
            ELSE 0
        END) AS points,
        COUNT(*) AS matches_played,
        SUM(CASE WHEN away_goals > home_goals THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN away_goals = home_goals THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN away_goals < home_goals THEN 1 ELSE 0 END) AS losses,
        SUM(away_goals) AS goals_for,
        SUM(home_goals) AS goals_against
    FROM {{ ref('stg_pl_2425') }}
    GROUP BY away_team
),
standings AS (
    SELECT
        team,
        SUM(points) AS points,
        SUM(matches_played) AS matches_played,
        SUM(wins) AS wins,
        SUM(draws) AS draws,
        SUM(losses) AS losses,
        SUM(goals_for) AS goals_for,
        SUM(goals_against) AS goals_against,
        SUM(goals_for) - SUM(goals_against) AS goal_difference
    FROM match_points
    GROUP BY team
)
SELECT
    team,
    matches_played,
    wins,
    draws,
    losses,
    goals_for,
    goals_against,
    goal_difference,
    points,
    RANK() OVER (ORDER BY points DESC, goal_difference DESC, goals_for DESC) AS position
FROM standings
ORDER BY position