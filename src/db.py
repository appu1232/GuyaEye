import psycopg2, hashlib, time, os


class Database:

    def __init__(self, host = None, port = None, username = None, password = None, dbname = None):
        self.host = host or os.getenv('DB_HOST')
        self.port = port or os.getenv('DB_PORT')
        self.username = username or os.getenv('DB_USER')
        self.password = password or os.getenv('DB_PASS')
        self.dbname = dbname or os.getenv('DB_NAME')
        
        self.connect_to_database()

    def connect_to_database(self):
        self.db = psycopg2.connect(
            host = self.host,
            port = self.port,
            user = self.username,
            password = self.password,
            dbname = self.dbname
        )

        self.cursor = self.db.cursor()
        self.create_tables()

    def create_tables(self):
        encoding_sql = "CREATE TABLE IF NOT EXISTS encodings (id text PRIMARY KEY, label text, hash bytea)"

        self.cursor.execute(encoding_sql)
        self.db.commit()

    def truncate(self):
        sql = "TRUNCATE TABLE encodings;"
        self.cursor.execute(sql)
        self.db.commit()

    def store_encoding(self, label, encoding):
        id = self.sha256(str(label + str(time.time())).encode("utf-8"))
        sql = "INSERT INTO encodings (id, label, hash) VALUES ('{}', '{}', '\\x{}')".format(id, label, encoding)
        self.cursor.execute(sql)
        self.db.commit()

    def compare_encoding(self, encoding):
        sql = "SELECT encs.label, encs.distance FROM (SELECT label,  ((get_byte(hash, 11) * 65536 + get_byte(hash, 12) * 256 + get_byte(hash, 13)) - ((get_byte('\\x{}', 11) * 65536 + get_byte('\\x{}', 12) * 256 + get_byte('\\x{}', 13)))) as distance FROM encodings) AS encs WHERE encs.distance >= 0 GROUP BY encs.label, encs.distance ORDER BY encs.distance ASC LIMIT 10".format(encoding, encoding, encoding)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def sha256(self, text):
        m = hashlib.sha256()
        m.update(str(text).encode('utf-8'))
        m.update(str(time.time()).encode('utf-8'))
        return m.hexdigest()