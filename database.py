import sqlite3


def create_db():
    conn = sqlite3.connect('homework.db')  # Создаем (или открываем) базу данных
    cursor = conn.cursor()

    # Создаем таблицу homeworks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS homeworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            homework_number INTEGER NOT NULL,
            github_link TEXT NOT NULL
        )
    ''')

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение


def save_homework(name, group_name, homework_number, github_link):
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO homeworks (name, group_name, homework_number, github_link) VALUES (?, ?, ?, ?)',
                   (name, group_name, homework_number, github_link))

    conn.commit()
    conn.close()
