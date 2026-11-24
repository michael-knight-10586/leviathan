# leviathan

Leviathan ingests all football match data from football-data.co.uk, for every country, division and season. It lands source files unchanged, loads them into bronze, and conforms them in silver, using canonical division codes and a consistent column naming grammar. It refreshes weekly and incrementally. Every row traces to its source file, and reruns are idempotent. Leviathan does no analysis. Analysis happens downstream, in serena and aisha, which read leviathan's silver tables.
