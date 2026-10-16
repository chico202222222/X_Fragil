import sqlite3
import os

SRC = os.path.join(os.path.dirname(__file__), '..', '..', '..')
DB_FILE = os.path.join(SRC, 'prisma', 'dev.db')
# mock_db = mock database
# arquivo nao deve ser versionado, só em ambiente de desenvolvimento.

class MockDB:
    def __init__(self):
        self.conn = None
    def open(self):
        self.conn = sqlite3.connect('mock.db')
    def close(self):
        if self.conn is not None:
            self.conn.close()
    def insert(self, name, email, password):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        self.conn.commit()
        return cursor.lastrowid
    def select(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()

if __name__ == '__main__':
    mock_db = MockDB()
    mock_db.open()
    mock_db.insert('teste', 'teste@usuario.com', '123456')
    print(mock_db.select('teste@usuario.com'))
    mock_db.close()