CREATE TABLE games (id SERIAL PRIMARY KEY, home_team TEXT, visitor_team TEXT, date TIMESTAMP, outcome_added INTEGER);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin INTEGER);

CREATE TABLE scores (id SERIAL PRIMARY KEY, game_id INTEGER REFERENCES games, user_id INTEGER REFERENCES users, scores INTEGER);

CREATE TABLE bets (id SERIAL PRIMARY KEY, game_id INTEGER REFERENCES games, user_id INTEGER REFERENCES users, goals_home INTEGER, goals_visitor INTEGER);

CREATE TABLE outcomes (id SERIAL PRIMARY KEY, game_id INTEGER REFERENCES games UNIQUE, goals_home INTEGER, goals_visitor INTEGER, scored INTEGER);




