import psycopg2
from psycopg2 import sql
from typing import Optional, Tuple
from psycopg2.extensions import connection
from selenium.webdriver.common.by import By

def collect_stat_wallet() -> None:
    """Данные кошелька в БД"""
    global driver
    try:
        wallet_amount = float(driver.find_element(By.CLASS_NAME, '_relative--TTwjI').text)
        save_wallet_statistic(wallet_amount)
    except:
        print(f'Данные в кошельке не обновлены \n{e}')

def connect_db() -> connection:
    # Общая функция для подключения к БД
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="user",
        password="password",
        host="db",
        port="5432"
    )
    return conn

def close_db(conn, cur):
    # Общая функция для закрытия соединения с БД
    cur.close()
    conn.close()

def create_tables_if_not_exists() -> None:
    """Создает таблицы wallet_db и stat_bet, если они не существуют."""
    conn = connect_db()
    cur = conn.cursor()

    create_tables_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS wallet_db (
            id SERIAL PRIMARY KEY,
            bet_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            wallet_amount FLOAT NOT NULL );

        CREATE TABLE IF NOT EXISTS stat_bet (
            id SERIAL PRIMARY KEY,
            bet_amount FLOAT NOT NULL,
            existed BOOLEAN DEFAULT TRUE );
                                            """)

    cur.execute(create_tables_query)
    conn.commit()
    close_db(conn, cur)

def collect_stat_bet(bet_amount: float, existed: bool) -> None:
    """Вставляет запись о ставке в таблицу stat_bet."""
    conn = connect_db()
    cur = conn.cursor()

    insert_query = sql.SQL("""INSERT INTO stat_bet (bet_amount, existed) VALUES (%s, %s)""")

    cur.execute(insert_query, (bet_amount, existed))
    conn.commit()
    close_db(conn, cur)

def insert_wallet_statistic(wallet_amount: float) -> None:
    """Вставляет запись о состоянии кошелька в таблицу wallet_db."""
    conn = connect_db()
    cur = conn.cursor()

    insert_query = sql.SQL("""INSERT INTO wallet_db (wallet_amount) VALUES (%s)""")

    cur.execute(insert_query, (wallet_amount,))
    conn.commit()
    close_db(conn, cur)

def get_latest_wallet_statistic() -> Optional[Tuple]:
    """Возвращает последнюю запись о состоянии кошелька"""
    conn = connect_db()
    cur = conn.cursor()

    select_query = sql.SQL("""SELECT * FROM wallet_db ORDER BY bet_date DESC LIMIT 1""")

    cur.execute(select_query)
    latest_record = cur.fetchone()
    close_db(conn, cur)

    return latest_record

def save_wallet_statistic(current_wallet_amount: float) -> Optional[Tuple]:
    """
    Сохраняет текущее состояние кошелька, если оно выше последнего записанного в таблицу.
    Возвращает последнюю запись о состоянии кошелька.
    """
    latest_record = get_latest_wallet_statistic()
    if latest_record and current_wallet_amount > latest_record[2]:
        insert_wallet_statistic(current_wallet_amount)

    return latest_record

def get_latest_wallet_statistic() -> Optional[Tuple]:
    """Возвращает последнюю запись о состоянии кошелька из таблицы wallet_db."""
    conn = connect_db()
    cur = conn.cursor()

    select_query = sql.SQL("""SELECT * FROM wallet_db ORDER BY bet_date DESC""")
    cur.execute(select_query)
    wallet = cur.fetchall()

    close_db(conn, cur)
    return wallet

if __name__ == "__main__":
    create_tables_if_not_exists()

    insert_wallet_statistic(200.0)

    latest_record = save_wallet_statistic(300.0)
    print("Самая актуальная запись:", latest_record)

    all_records = get_latest_wallet_statistic()
    print("Все записи:", all_records)