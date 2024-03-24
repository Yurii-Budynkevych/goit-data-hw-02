import sqlite3

create_table_query = """
CREATE TABLE genders (
  id INT PRIMARY KEY,
  name VARCHAR(30),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

fill_table_query = """
INSERT INTO genders (id, name)
VALUES (1, 'male'), (2, 'female');
"""

select_info_query = """
SELECT * FROM genders;
"""

connection = sqlite3.connect('test.db')
cursor = connection.cursor()

cursor.execute(create_table_query)
cursor.execute(fill_table_query)
connection.commit()

cursor.execute(select_info_query)
result = cursor.fetchall()
print(result)

cursor.close()
connection.close()