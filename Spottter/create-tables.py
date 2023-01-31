import psycopg2

conn = psycopg2.connect(host="database.rhodescs.org", user="ellje-23", password="ellje-23", dbname="practice")
cur = conn.cursor()  # make a cursor (allows us to execute queries)

file = open("schema.sql", "r") # open the file
alltext = file.read() # read all the text
cur.execute(alltext) # execute all the SQL in the file
conn.commit()  # Actually make the changes to the db

cur.close()  
conn.close() # close everything