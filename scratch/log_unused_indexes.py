import psycopg2
import csv
import os
import datetime

# --- Configuration ---
# The log file will be created in the same directory as the script.
LOG_FILE = 'unused_indexes_log.csv'

# The query to find unused indexes.
# It excludes primary key and unique constraints for safety.
UNUSED_INDEX_QUERY = """
SELECT
	s.schemaname,
	s.relname AS tablename,
	s.indexrelname AS indexname,
	pg_size_pretty(pg_relation_size(s.indexrelid)) AS index_size,
	s.idx_scan
FROM
	pg_stat_user_indexes s
JOIN
	pg_index i ON s.indexrelid = i.indexrelid
WHERE
	s.idx_scan = 0
	AND i.indisunique = false
	AND i.indisprimary = false
ORDER BY
	pg_relation_size(s.indexrelid) DESC;
"""

def get_db_connection():
	"""Establishes a database connection using environment variables."""
	try:
		conn = psycopg2.connect(
			dbname=os.environ.get('DB_NAME'),
			user=os.environ.get('DB_USER'),
			password=os.environ.get('DB_PASSWORD'),
			host=os.environ.get('DB_HOST'),
			port=os.environ.get('DB_PORT')
		)
		return conn
	except psycopg2.OperationalError as e:
		print(f"Error: Could not connect to the database. {e}")
		print("Please ensure database credentials are set as environment variables.")
		return None

def log_unused_indexes():
	"""
	Executes the query to find unused indexes and logs the results
	to a CSV file with a timestamp.
	"""
	conn = get_db_connection()
	if not conn:
		return

	print("Successfully connected to the database. Running query...")

	try:
		with conn.cursor() as cur:
			cur.execute(UNUSED_INDEX_QUERY)
			results = cur.fetchall()

			if not results:
				print("No unused indexes found.")
				return

			print(f"Found {len(results)} unused indexes. Logging to {LOG_FILE}...")

			# Check if file exists to determine if we need to write headers
			file_exists = os.path.isfile(LOG_FILE)

			with open(LOG_FILE, 'a', newline='') as csvfile:
				writer = csv.writer(csvfile)

				# Write headers if the file is new
				if not file_exists:
					headers = ['log_timestamp', 'schema_name', 'table_name', 'index_name', 'index_size', 'scan_count']
					writer.writerow(headers)

				# Write data rows with the current timestamp
				log_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
				for row in results:
					writer.writerow([log_timestamp] + list(row))

			print("Logging complete.")

	except (Exception, psycopg2.Error) as error:
		print(f"Error while fetching data from PostgreSQL: {error}")
	finally:
		# Ensure the connection is closed
		if conn:
			conn.close()
			print("Database connection closed.")

if __name__ == "__main__":
	log_unused_indexes()
