create table if not exists users (
  u_id serial primary key
);
create index if not exists users_u_id_idx on users (u_id);

create table if not exists wallets (
  w_id serial primary key,
  w_user_id integer not null unique references users (u_id),
  w_balance numeric not null default 0
);
create index if not exists wallets_w_id_idx on wallets (w_id);
create index if not exists wallets_w_user_id_idx on wallets (w_user_id);

create table if not exists transactions (
  t_id serial primary key,
  t_wallet_id integer not null references wallets (w_id),
  t_user_id integer not null references users (u_id),
  t_timestamp timestamp not null default current_timestamp,
  t_volume numeric not null
);
create index if not exists transactions_t_id_idx on transactions (t_id);
create index if not exists transactions_t_wallet_id_idx on transactions (t_wallet_id);
create index if not exists transactions_t_user_id_idx on transactions (t_user_id);