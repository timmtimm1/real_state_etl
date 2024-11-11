import pandas as pd
import psycopg2
from psycopg2 import Error
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_import.log'),
        logging.StreamHandler()
    ]
)

def create_database():
    """Create the database and required tables"""
    
    # Database connection parameters
    db_params = {
        "host": "localhost",
        "database": "postgres",  # Connect to default db first
        "user": "postgres",
        "password": "Bb121973820@"
    }
    
    try:
        logging.info("Attempting to create database and tables...")
        
        # Connect to default database first
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'real_estate_db'")
        if not cur.fetchone():
            cur.execute("CREATE DATABASE real_estate_db")
            logging.info("Database 'real_estate_db' created successfully")
        else:
            logging.info("Database 'real_estate_db' already exists")
        
        # Close connection to default database
        cur.close()
        conn.close()
        
        # Connect to our new database
        db_params["database"] = "real_estate_db"
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # Create locations table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                location_id SERIAL PRIMARY KEY,
                neighborhood VARCHAR(100),
                city VARCHAR(100),
                state VARCHAR(2),
                cep VARCHAR(8),
                UNIQUE (neighborhood, city, state, cep)
            )
        """)
        logging.info("Locations table created/verified")
        
        # Create price_categories table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS price_categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(50) UNIQUE
            )
        """)
        logging.info("Price categories table created/verified")
        
        # Create properties table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                property_id SERIAL PRIMARY KEY,
                price NUMERIC(12,2),
                price_per_m2 NUMERIC(12,2),
                area_util NUMERIC(8,2),
                bedrooms SMALLINT,
                bathrooms SMALLINT,
                parking_spots SMALLINT,
                location_id INTEGER REFERENCES locations(location_id),
                category_id INTEGER REFERENCES price_categories(category_id),
                scraped_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logging.info("Properties table created/verified")
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_properties_price ON properties(price)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_properties_area ON properties(area_util)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_locations_cep ON locations(cep)")
        logging.info("Indexes created/verified")
        
        conn.commit()
        return conn, cur
    
    except (Exception, Error) as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")
        return None, None

def insert_data(conn, cur, data_path):
    """Insert data from CSV into the database"""
    
    try:
        logging.info(f"Reading data from: {data_path}")
        
        # Verify file exists
        if not os.path.exists(data_path):
            logging.error(f"File not found: {data_path}")
            return
        
        # Read CSV file
        df = pd.read_csv(data_path)
        logging.info(f"Successfully read {len(df)} rows from CSV")
        
        # Clean and prepare data
        df['cep'] = df['cep'].fillna(0).astype(int).astype(str).str.replace('.0', '')
        df = df.replace({pd.NA: None, float('nan'): None})
        
        # Insert price categories
        categories = df['price_category'].unique()
        logging.info(f"Found {len(categories)} unique price categories")
        
        for category in categories:
            cur.execute(
                "INSERT INTO price_categories (category_name) VALUES (%s) ON CONFLICT (category_name) DO NOTHING",
                (category,)
            )
        
        # Get category mappings
        cur.execute("SELECT category_name, category_id FROM price_categories")
        category_mapping = dict(cur.fetchall())
        
        # Insert locations and properties
        successful_inserts = 0
        failed_inserts = 0
        
        for idx, row in df.iterrows():
            try:
                # Insert location
                cur.execute("""
                    INSERT INTO locations (neighborhood, city, state, cep)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (neighborhood, city, state, cep) DO UPDATE
                    SET neighborhood = EXCLUDED.neighborhood
                    RETURNING location_id
                """, (row['neighborhood'], row['city'], row['state'], row['cep']))
                
                location_id = cur.fetchone()[0]
                
                # Insert property
                cur.execute("""
                    INSERT INTO properties (
                        price, price_per_m2, area_util, bedrooms, bathrooms,
                        parking_spots, location_id, category_id, scraped_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['price'],
                    row['price_per_m2'],
                    row['area_util'],
                    row['quartos'],
                    row['banheiros'],
                    row['vagas'],
                    location_id,
                    category_mapping[row['price_category']],
                    datetime.strptime(row['scraped_date'], '%Y-%m-%d').date()
                ))
                
                successful_inserts += 1
                
                # Log progress every 1000 rows
                if successful_inserts % 1000 == 0:
                    logging.info(f"Processed {successful_inserts} rows successfully")
                    conn.commit()
                
            except Exception as e:
                failed_inserts += 1
                logging.error(f"Error inserting row {idx}: {e}")
                continue
        
        conn.commit()
        logging.info(f"Data insertion completed. Successful: {successful_inserts}, Failed: {failed_inserts}")
        
    except (Exception, Error) as error:
        conn.rollback()
        logging.error(f"Error while inserting data: {error}")

def main():
    # Define the data path
    data_path = r"C:\Users\berna\etl_project\data\interim\properties_cleaned_no_outliers.csv"
    
    # Create database and tables
    conn, cur = create_database()
    if conn and cur:
        try:
            # Insert data
            insert_data(conn, cur, data_path)
        finally:
            # Close database connection
            cur.close()
            conn.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()