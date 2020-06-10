import psycopg2
from parser import parse
import pdb
from tqdm import tqdm

HOST = "localhost"
DATABASE = "cs166"
USER = "madisoncoots"
PASSWORD = ""

WAR_AND_PEACE = "http://www.gutenberg.org/files/2600/2600-0.txt"
ULYSSES = "http://www.gutenberg.org/files/4300/4300-0.txt"
SHAKESPEARE = "http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt"

def main():

	# sql_1 = "INSERT INTO war_and_peace(token) VALUES(%s)"
	# print("Connecting to " + DATABASE + "...")
	# conn = psycopg2.connect(host=HOST,database=DATABASE, user=USER, password=PASSWORD)
	# cur = conn.cursor()
	# tokens = parse(WAR_AND_PEACE)
	# for i in tqdm(range(len(tokens))):
	# 	cur.execute(sql, (tokens[i],))
	# conn.commit()
	# cur.close()
	# conn.close()

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

	sql_3 = "INSERT INTO shakespeare(token) VALUES(%s)"
	print("Connecting to " + DATABASE + "...")
	conn = psycopg2.connect(host=HOST,database=DATABASE, user=USER, password=PASSWORD)
	cur = conn.cursor()
	tokens = parse(SHAKESPEARE)
	for i in tqdm(range(len(tokens))):
		cur.execute(sql_3, (tokens[i],))
	conn.commit()
	cur.close()
	conn.close()



if __name__ == '__main__':
	main()
