do $$
begin
    create type transaction_type as enum (
        'deposit',
        'withdraw',
        'transfer'
    );
exception
    when duplicate_object then null;
end
$$;

create table if not exists accounts (
    id integer generated always as identity primary key,
    owner text not null,
    balance integer not null default 0 check(balance >= 0)
);

create table if not exists transactions (
    id integer generated always as identity primary key,
    type transaction_type not null,
    amount integer not null check(amount > 0),
    from_account_id integer references accounts(id),
    to_account_id integer references accounts(id),
    created_at timestamptz not null default now()
);