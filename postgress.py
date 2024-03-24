import psycopg2
from faker import Faker

fake = Faker()

# query
create_table_query = """
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100),
  email VARCHAR(100) UNIQUE
);
"""

create_table_query1 = """
CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE
);
"""

create_table_query2 = """
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status_id INT REFERENCES status (id) ON DELETE SET NULL ON UPDATE CASCADE,
  user_id INT REFERENCES users (id) ON DELETE SET NULL ON UPDATE CASCADE
);
"""

join_info_query = """
SELECT tasks.id, tasks.title, tasks.description, status.name AS status_name, users.fullname AS user_name
FROM tasks
LEFT JOIN status ON tasks.status_id = status.id
LEFT JOIN users ON tasks.user_id = users.id;
"""

select_info_query = """
SELECT * FROM tasks;
"""

# connect
connection = psycopg2.connect(
    database="", user='postgres',
    password='password', host='localhost', port=5432
)

cursor = connection.cursor()

cursor.execute(create_table_query)
connection.commit()
cursor.execute(create_table_query1)
connection.commit()

# fill statuses
status_data = ['new', 'in progress', 'completed']
for status in status_data:
    cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))
connection.commit()
# end fill statuses

cursor.execute(create_table_query2)
connection.commit()

# fill rest
# 1
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    connection.commit()

# 3
task1 = ('do this', 'do this first', 1, 2)
task2 = ('do that', 'do that second', 2, 2)
cursor.execute(
    "INSERT INTO tasks (title, description, status_id, user_id) "
    "VALUES (%s, %s, %s, %s)",
    (task1[0], task1[1], task1[2], task1[3])
)
connection.commit()

cursor.execute(
    "INSERT INTO tasks (title, description, status_id, user_id) "
    "VALUES (%s, %s, %s, %s)",
    (task2[0], task2[1], task2[2], task2[3])
)  
connection.commit() 

# join
cursor.execute(join_info_query)
result = cursor.fetchall()
print(result)

cursor.close()
connection.close()