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
