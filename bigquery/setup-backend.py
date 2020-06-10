#import psycopg2
#from parser import parse
#import pdb
#from tqdm import tqdm
import pandas as pd
import prestodb.dbapi as presto
#import MySQLdb


HOST = "localhost"
DATABASE = "hll_test_library"
USER = "Surya"
PASSWORD = ""

WAR_AND_PEACE = "http://www.gutenberg.org/files/2600/2600-0.txt"
ULYSSES = "http://www.gutenberg.org/files/4300/4300-0.txt"
SHAKESPEARE = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"

def main():

	
	sql_1 = "INSERT INTO wandp(words) VALUES(%s)"
	#print("Connecting to " + DATABASE + "...")

	# conn=prestodb.dbapi.connect(
	# 	host='localhost',
	# 	port=5432,
	# 	user=USER
	# )

	conn = presto.Connection(host="localhost", port=5433, user=USER)

	cur = conn.cursor()

	print(cur)

	cur.execute("SHOW catalogs")
	cur.fetchall()
	
	#cur.execute("SELECT COUNT(*) FROM (SELECT DISTINCT words FROM wandp) AS temp")
	#rows = cur.fetchall()

	#cur.execute("""
	#CREATE TABLE wandp (words VARCHAR (50) NOT NULL)""", async_=True)	
	
	#tokens = parse(WAR_AND_PEACE)
	#for i in tqdm(range(len(tokens))):
	#	cur.execute(sql_1, (tokens[i],))
	
	#cur.execute("""
	#SELECT COUNT(*) FROM (SELECT DISTINCT words FROM wandp) AS temp; """)
	
	#df = pd.DataFrame(cur.fetchall())

	#cur.execute("""
	#SELECT approx_distinct(words) FROM wandp; """)

	# sql_2 = "INSERT INTO ulysses(token) VALUES(%s)"
	# print("Connecting to " + DATABASE + "...")
	# conn = psycopg2.connect(host=HOST,database=DATABASE, user=USER, password=PASSWORD)
	# cur = conn.cursor()
	# tokens = parse(ULYSSES)
	# for i in tqdm(range(len(tokens))):
	# 	cur.execute(sql_2, (tokens[i],))
	# conn.commit()
	# cur.close()
	# conn.close()

	# sql_3 = "INSERT INTO shakespeare(token) VALUES(%s)"
	# print("Connecting to " + DATABASE + "...")
	# conn = psycopg2.connect(host=HOST,database=DATABASE, user=USER, password=PASSWORD)
	# cur = conn.cursor()
	# tokens = parse(SHAKESPEARE)
	# for i in tqdm(range(len(tokens))):
	# 	cur.execute(sql_3, (tokens[i],))
	# conn.commit()
	# cur.close()
	# conn.close()



if __name__ == '__main__':
	main()
