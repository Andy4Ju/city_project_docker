import time
import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# 讀取資料庫設定
db_user = os.getenv("MYSQL_USER", "root")
db_pass = os.getenv("MYSQL_PASSWORD", "P%40ssw0rd") # root
db_host = os.getenv("MYSQL_HOST", "localhost") # city_mysql
db_port = os.getenv("MYSQL_PORT", "3306")
db_name = os.getenv("MYSQL_DATABASE", "city")

DB_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

MAX_RETRIES = 10
WAIT_TIME = 3

# 建立連線
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DB_URI)
        with engine.connect():
            print(f"Connected to MySQL at {db_host}:{db_port}, DB: {db_name}")
            break
    except OperationalError as e:
        print(f"Attempt {attempt+1} failed, retrying in {WAIT_TIME}s... ({e})")
        time.sleep(WAIT_TIME)
else:
    print("Failed to connect to MySQL.")
    exit(1)

# ====== 自動抓取 table 欄位 ======
def get_table_columns(table_name: str) -> list[str]:
    query = f"SHOW COLUMNS FROM {table_name}"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        # row[0] 對應欄位名稱（Field）
        return [row[0] for row in result]

# ====== 生成 SQL 語法 ======
def generate_insert_sql(table_name: str, columns: list[str]) -> str:
    cols = ", ".join(columns)
    placeholders = ", ".join([f":{c}" for c in columns])
    updates = ", ".join([f"{c} = VALUES({c})" for c in columns])
    return f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {updates}"

# ====== CSV 資料夾 ======
CSV_DIR = Path("./csv")
csv_files = list(CSV_DIR.glob("*.csv"))
if not csv_files:
    print("⚠️ No CSV files found in ./csv/")
    exit(1)

# ====== 匯入 CSV ======
for csv_path in csv_files:
    table_name = csv_path.stem
    try:
        columns = get_table_columns(table_name)
    except Exception as e:
        print(f"⚠️ Could not get columns for table '{table_name}': {e}")
        continue

    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
        # 清理欄位名稱
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        columns_clean = [c.strip().lower().replace(" ", "_") for c in columns]
        df = df[[c for c in df.columns if c in columns_clean]]

        if df.empty:
            print(f"⚠️ CSV '{csv_path.name}' has no matching columns, skipping.")
            continue

        # 將 NaN 轉成 None
        df = df.where(pd.notnull(df), None)

        print(f"Reading '{csv_path.name}', records: {len(df)}")
        sql = generate_insert_sql(table_name, df.columns.tolist())
        with engine.begin() as conn:
            conn.execute(text(sql), df.to_dict(orient="records"))

        print(f"✅ Successfully imported '{csv_path.name}' into table '{table_name}'")

    except Exception as e:
        print(f"❌ Import failed for '{csv_path.name}': {e}")