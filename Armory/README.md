# Leviathan Armory: Feature Engineering Layers

This folder contains transformed data used as input features for predictive modeling.

- CrowsNest: League-wide scoring systems and observational signals
- Whaleboat: League table data, cumulative points
- Tackle: Context-aware adjustments (e.g., home advantage)
- Line: Basic team superiority model
- Harpoon: Advanced superiority and rating-based signals

Outputs Summary: Match Points & League Tables

This folder contains derived match-level and season-level team summaries used in the Leviathan project.

Final Outputs:

- Plankton_match_points.csv:
  Adds HomePoints and AwayPoints (1 = win, 0.5 = draw, 0 = loss) to each match.
  
- league_tables_by_season.csv:
  League table for each season, with total points, games played, and average points per match.

- team_points_summary_all_seasons.csv:
  Summary of team performance across all seasons. Includes total points, average points per season, and number of seasons played.

These outputs form the core data for further modeling in the Armory stage of the Leviathan pipeline.

