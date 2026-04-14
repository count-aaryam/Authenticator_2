import psycopg2

def init_table():
    conn = psycopg2.connect(
        host="localhost",
        dbname="demo_project",
        user="postgres",
        password="030405",
        port="5432"
    )
    cur=conn.cursor()
    cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
            CREATE TYPE user_role AS ENUM ('member', 'librarian', 'admin');
        END IF;
    END$$;
    """)

    cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'account_status_type') THEN
            CREATE TYPE account_status_type AS ENUM ('active', 'inactive', 'suspended');
        END IF;
    END$$;
    """)
    cur.execute(""" 
    CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'member',
    account_status account_status_type DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("table created succesfully")


if __name__=="__main__":
    init_table()


