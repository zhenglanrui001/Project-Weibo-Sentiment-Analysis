from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/db_weibo"
)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchone())
        print("数据库连接成功！")
except Exception as e:
    print("连接失败：", e)