CREATE TABLE users(id text primary key, password text);
CREATE TABLE ssids(user_id text, ssid text, password text, foreign key(user_id) references users(id), primary key(user_id, ssid));
