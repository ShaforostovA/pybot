from sqlalchemy.engine import URL

DB_PATH = URL.create(
    drivername="postgresql",
    username="oleg",
    password="447921",
    port="5432",
    host="localhost",
    database="pybot"
)
# f'postgresql://{"oleg"}:{"447921"}@{"localhost"}:{"5432"}/{"pybot"}'