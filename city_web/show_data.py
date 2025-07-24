import os
import time
import pandas as pd
import pymysql
from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__, static_folder="static", template_folder="templates")

# 資料庫連線設定
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),  # or docker: city_mysql
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "P@ssw0rd"), # root
    "database": os.environ.get("MYSQL_DATABASE", "city_study"),
}

# 封裝 pymysql.connect()
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# 預設空資料
df = pd.DataFrame()

# 加入 retry 機制
MAX_RETRY = 10
for i in range(MAX_RETRY):
    try:
        print(f"第 {i + 1} 次嘗試連線到資料庫...")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM cr", conn)
        conn.close()
        print(f"成功載入資料，共 {len(df)} 筆")
        break
    except Exception as e:
        print("資料庫連線失敗：", e)
        time.sleep(3)
else:
    print("無法連接資料庫，df 將保持空")

# -----------------------------------
# Flask 路由設定
# -----------------------------------

# index 頁面
@app.route("/")
def index():
    return render_template("index.html")

##############
# 角色 - 主頁 #
##############

# rocket-dev 頁面
@app.route("/rocket-dev-new")
def rocket_dev_new():
    return render_template("rocket-dev-new.html")

# steady-pro 頁面
@app.route("/steady-pro-new")
def steady_pro_new():
    return render_template("steady-pro-new.html")

# nomad-coder 頁面
@app.route("/nomad-coder-new")
def nomad_coder_new():
    return render_template("nomad-coder-new.html")

# startup-maverick 頁面
@app.route("/startup-maverick-new")
def startup_maverick_new():
    return render_template("startup-maverick-new.html")

##############
# 城市 - 主頁 #
##############

# new-york-city 頁面
@app.route("/new-york-city")
def new_york_city():
    return render_template("new-york-city.html")

# san-francisco 頁面
@app.route("/san-francisco")
def san_francisco():
    return render_template("san-francisco.html")

# london 頁面
@app.route("/london")
def london():
    return render_template("london.html")

# singapore 頁面
@app.route("/singapore")
def singapore():
    return render_template("singapore.html")

# sydney 頁面
@app.route("/sydney")
def sydney():
    return render_template("sydney.html")

# vancouver 頁面
@app.route("/vancouver")
def vancouver():
    return render_template("vancouver.html")

# seoul 頁面
@app.route("/seoul")
def seoul():
    return render_template("seoul.html")

# tokyo 頁面
@app.route("/tokyo")
def tokyo():
    return render_template("tokyo.html")

# taipei 頁面
@app.route("/taipei")
def taipei():
    return render_template("taipei.html")

# bangkok 頁面
@app.route("/bangkok")
def bangkok():
    return render_template("bangkok.html")

# hong-kong 頁面
@app.route("/hong-kong")
def hong_kong():
    return render_template("hong-kong.html")

##############
# 指標 一覽表 #
##############

# career-velocity-index 頁面
@app.route("/career-velocity-index")
def career_velocity_index():
    return render_template("career-velocity-index.html")

# coworking-space 頁面
@app.route("/coworking-space")
def coworking_space():
    return render_template("coworking-space.html")

# global-tech-env 頁面
@app.route("/global-tech-env")
def global_tech_env():
    return render_template("global-tech-env.html")

# healthcare-cost 頁面
@app.route("/healthcare-cost")
def healthcare_cost():
    return render_template("healthcare-cost.html")

# job-vacancy 頁面
@app.route("/job-vacancy")
def job_vacancy():
    return render_template("job-vacancy.html")

# rent-comparison 頁面
@app.route("/rent-comparison")
def rent_comparison():
    return render_template("rent-comparison.html")


##################
# 角色-Top3 City #
##################

@app.route("/api/ch1_top3")
def get_ch1_top3():
    try:
        conn = get_connection()
        query = """
            SELECT s.city_id, c.english_name, c.chinese_name, s.total
            FROM view_ch1_score s
            JOIN city_name c ON s.city_id = c.city_id
            ORDER BY s.total DESC
            LIMIT 3
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print("讀取 view_ch1_score 失敗：", e)
        return jsonify([]), 500

@app.route("/api/ch2_top3")
def get_ch2_top3():
    try:
        conn = get_connection()
        query = """
            SELECT s.city_id, c.english_name, c.chinese_name, s.scaled_total AS total
            FROM view_ch2_score s
            JOIN city_name c ON s.city_id = c.city_id
            ORDER BY s.scaled_total DESC
            LIMIT 3
        """
        df_ch2_top3 = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df_ch2_top3.to_dict(orient="records"))
    except Exception as e:
        print("讀取 view_ch2_score 失敗：", e)
        return jsonify([]), 500

@app.route("/api/ch3_top3")
def get_ch3_top3():
    try:
        conn = get_connection()
        query = """
            SELECT s.city_id, c.english_name, c.chinese_name, s.total
            FROM view_ch3_score s
            JOIN city_name c ON s.city_id = c.city_id
            ORDER BY s.total DESC
            LIMIT 3
        """
        df_ch3_top3 = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df_ch3_top3.to_dict(orient="records"))
    except Exception as e:
        print("讀取 view_ch2_score 失敗：", e)
        return jsonify([]), 500
    
@app.route("/api/ch4_top3")
def get_ch4_top3():
    try:
        conn = get_connection()
        query = """
            SELECT s.city_id, c.english_name, c.chinese_name, s.total
            FROM view_ch4_score s
            JOIN city_name c ON s.city_id = c.city_id
            ORDER BY s.total DESC
            LIMIT 3
        """
        df_ch4_top3 = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df_ch4_top3.to_dict(orient="records"))
    except Exception as e:
        print("讀取 view_ch4_score 失敗：", e)
        return jsonify([]), 500

##################
#  角色-Features  #
##################


@app.route("/api/ch1_feature_raw_top3")
def ch1_feature_raw_top3():
    field = request.args.get("field")

    # 定義要查的 table、欄位、單位
    table_map = {
        "salary": ("sal", "ju_med", "USD"),
        "rent": ("city_study.view_rental", "avg_ppsqm", "USD/m²"),
        "vacancy": ("vac", "junior", "件")
    }

    if field not in table_map:
        return jsonify([])

    table, column, unit = table_map[field]

    query = f"""
        SELECT c.city_id, c.english_name, c.chinese_name, ROUND(t.{column}, 0) AS value
        FROM {table} t
        JOIN city_name c ON t.city_id = c.city_id
        ORDER BY t.{column} DESC
        LIMIT 3
    """

    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()

        # 加上單位傳回
        df["unit"] = unit
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print(f"讀取 raw feature 失敗：{e}")
        return jsonify([]), 500


# 角色2 - features
@app.route("/api/ch2_feature_raw_top3")
def ch2_feature_raw_top3():
    field = request.args.get("field")

    # 定義角色二對應的 table、欄位、單位
    table_map = {
        "salary": ("sal", "se_med", "USD"),
        "health": ("health", "out_of_pocket_usd", "USD"),
        "company": ("comp_size", "total", "間")
    }

    if field not in table_map:
        return jsonify([])

    table, column, unit = table_map[field]

    # 若為 health 的 out_of_pocket_usd，排序應為 ASC（越低越好）
    order = "ASC" if field == "health" else "DESC"

    query = f"""
        SELECT c.city_id, c.english_name, c.chinese_name, ROUND(t.{column}, 0) AS value
        FROM {table} t
        JOIN city_name c ON t.city_id = c.city_id
        ORDER BY t.{column} {order}
        LIMIT 3
    """

    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()

        df["unit"] = unit
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print(f"讀取角色二 raw feature 失敗：{e}")
        return jsonify([]), 500

# 角色3 - features（查原始 feature 表格）
@app.route("/api/ch3_feature_raw_top3")
def ch3_feature_raw_top3():
    field = request.args.get("field")

    # 對應資料表、欄位、單位
    table_map = {
        "max_stay": ("nomad_visa", "max_stay", "月"),
        "net_speed": ("net_speed", "fixed_speed_mbps", "Mbps"),
        "cowork_index": ("coworking_index", "index_score", "分")
    }

    if field not in table_map:
        return jsonify([])

    table, column, unit = table_map[field]

    # 年份條件
    year_filter = "WHERE year = 2025" if table in ("nomad_visa", "net_speed") else "WHERE year = 2024"

    query = f"""
        SELECT c.city_id, c.english_name, c.chinese_name, ROUND(t.{column}, 2) AS value
        FROM {table} t
        JOIN city_name c ON t.city_id = c.city_id
        {year_filter}
        ORDER BY t.{column} DESC
        LIMIT 3
    """

    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()

        df["unit"] = unit
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print(f"讀取 raw feature 失敗：{e}")
        return jsonify([]), 500

    

# 角色4 - features
@app.route("/api/ch4_feature_raw_top3")
def ch4_feature_raw_top3():
    field = request.args.get("field")

    # 定義要查的 table、欄位、單位
    table_map = {
        "vc_funding": ("vc_funding", "vc_funding", "億美元"),
        "start_eco": ("start_eco", "start_eco", "分數"),
        "startup_count": ("startup_count", "startup_count", "家")
    }

    if field not in table_map:
        return jsonify([])

    table, column, unit = table_map[field]

    query = f"""
        SELECT c.city_id, c.english_name, c.chinese_name, ROUND(t.{column}, 0) AS value
        FROM {table} t
        JOIN city_name c ON t.city_id = c.city_id
        ORDER BY t.{column} DESC
        LIMIT 3
    """

    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()

        # 加上單位傳回
        df["unit"] = unit
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        print(f"讀取 raw feature 失敗：{e}")
        return jsonify([]), 500



@app.route("/new-character-design")
def new_character_design():
    return render_template("new-character-design.html")


@app.route("/feature/<feature_name>")
def get_feature_data(feature_name):
    city_id = request.args.get("city_id", "")
    year_id = request.args.get("year_id", "")
    print(f"取得 feature: {feature_name}, 篩選條件: city_id={city_id}, year_id={year_id}")

    try:
        conn = get_connection()
        df_feature = pd.read_sql(f"SELECT * FROM {feature_name}", conn)
        conn.close()
    except Exception as e:
        print(f"讀取資料表 {feature_name} 失敗：", e)
        return jsonify([]), 500

    # 篩選
    if city_id:
        df_feature = df_feature[df_feature["city_id"] == city_id]
    if year_id:
        try:
            year_id = int(year_id)
            df_feature = df_feature[df_feature["year_id"] == year_id]
        except ValueError:
            pass

    df_feature = df_feature.fillna("")
    return jsonify({"data": df_feature.to_dict(orient="records")})


# 改為用 pymysql 讀取資料庫 View
@app.route("/city/<city_id>/yearly")
def show_yearly(city_id):
    try:
        conn = get_connection()
        df_view = pd.read_sql(
            "SELECT * FROM view_city_yearly WHERE city_id = %s",
            conn,
            params=(city_id,)
        )
        conn.close()
    except Exception as e:
        print("讀取 View 失敗：", e)
        df_view = pd.DataFrame()

    return render_template("city_yearly.html", city_id=city_id, df=df_view)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
