DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS users CASCADE;

create table users (
    user_id serial primary key,
    name varchar(50) NOT NULL
);

create table accounts (
    account_id serial primary key,
    user_id integer,
    account_name varchar(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

create table transactions (
    transaction_id serial primary key,
    account_id integer,
    amount_cents integer NOT NULL,
    description varchar(50) NOT NULL,
    created_at date NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);