import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
    'users', metadata,

    sa.Column('u_id', sa.Integer, primary_key=True),
)

wallets = sa.Table(
    'wallets', metadata,

    sa.Column('w_id', sa.Integer, primary_key=True),
    sa.Column('w_user_id', sa.ForeignKey('users.u_id')),
    sa.Column('w_balance', sa.Numeric),
)

transactions = sa.Table(
    'transactions', metadata,

    sa.Column('t_id', sa.Integer, primary_key=True),
    sa.Column('t_wallet_id', sa.ForeignKey('wallets.w_id')),
    sa.Column('t_user_id', sa.ForeignKey('users.u_id')),
    sa.Column('t_timestamp', sa.DateTime),
    sa.Column('t_volume', sa.Numeric),
)
