create table user 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(255) not null,
    email varchar(255),
    password varchar(255) not null,
    theme jsonb,
    all_counters jsonb,
    constraint username unique (username) 
);

INSERT INTO user(username, email, password, theme, all_counters) VALUES
('sawcka', 'saw.cka@mail.ru', '123123123', '{
  "current": "dark",
  "isMenuVisible": false,
  "isSystemTheme": true
}', '[{"id":1667114174831,"title":"asd","description":"asd","counter":19,"goal":0,"defaultInput":1,"color":"#813d9c","textColor":"#ffffff"},{"id":1667114406447,"title":"от","description":"до","counter":0,"goal":0,"defaultInput":1,"color":"#ff9b41","textColor":"#000000"}]');

