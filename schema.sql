PRAGMA foreign_keys = ON;

create table if not exists accounts (
    id integer primary key autoincrement,
    owner text uniqie not null,
    balance integer not null default 0 check(balance >= 0)
);

create table if not exists transactions (
    id integer primary key autoincrement,
    type text not null check(type in ('deposit',  'withdraw', 'transfer')),
    amount int not null check(amount > 0),
    from_account_id integer,
    to_account_id integer,
    created_at text not null,

    foreign key(from_account_id) references accounts(id),
    foreign key(to_account_id) references accounts(id)
);