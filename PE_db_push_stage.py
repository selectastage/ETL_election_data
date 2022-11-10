import mariadb
import sys
import pandas as pd

cleaned_output = pd.read_csv('california_district_stats_src.csv')

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="cpi",
        password="HB_05ii",
        host="localhost",
        port=3306,
        database="cpi_project"
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# Create row tuples from Pandas data frame (required for SQL insertion)
cleaned_output_tup = list(zip(*map(cleaned_output.get, cleaned_output)))

# Create table in MariaDB & define data types
create_table = "CREATE TABLE IF NOT EXISTS california_cd_stats(congressional_district INT, population INT, people_per_square_mile INT, median_age FLOAT, percent_ethnicity_white FLOAT, percent_ethnicity_black FLOAT, percent_ethnicity_native FLOAT, percent_ethnicity_asian FLOAT, percent_ethnicity_islander FLOAT, percent_ethnicity_other FLOAT, percent_ethnicity_multiple FLOAT, percent_ethnicity_hispanic FLOAT, per_capita_income INT, median_household_income INT, percent_below_pov_per FLOAT, mean_commute_in_min FLOAT, percent_mode_of_transport_drove FLOAT, percent_mode_of_transport_carpooled FLOAT,percent_mode_of_transport_public FLOAT, percent_mode_of_transport_bicycle FLOAT, percent_mode_of_transport_walked FLOAT, house_count INT, pp_household FLOAT, percent_mother_past_year FLOAT, housing_units INT, median_house_price INT, percent_high_school_education_or_higher FLOAT, percent_secondary_education_or_higher FLOAT, percent_foreign_language_speakers FLOAT, share_of_young_voters FLOAT, share_of_middle_aged_voters FLOAT, share_of_senior_voters FLOAT);"

try: 
    cur.execute(create_table) 
    conn.commit()

except mariadb.Error as e: 
    print(f"Error: {e}")

# Insert information into MariaDB table
sql = "INSERT INTO california_cd_stats(congressional_district , population , people_per_square_mile , median_age , percent_ethnicity_white , percent_ethnicity_black , percent_ethnicity_native , percent_ethnicity_asian , percent_ethnicity_islander , percent_ethnicity_other , percent_ethnicity_multiple , percent_ethnicity_hispanic , per_capita_income , median_household_income , percent_below_pov_per , mean_commute_in_min , percent_mode_of_transport_drove ,percent_mode_of_transport_carpooled ,percent_mode_of_transport_public , percent_mode_of_transport_bicycle , percent_mode_of_transport_walked , house_count , pp_household , percent_mother_past_year , housing_units ,median_house_price , percent_high_school_education_or_higher , percent_secondary_education_or_higher , percent_foreign_language_speakers , share_of_young_voters , share_of_middle_aged_voters , share_of_senior_voters ) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s,%s, %s );"
    
try: 
    # Iterate through list of row tuples
    cur.executemany(sql, cleaned_output_tup)
    conn.commit()

except mariadb.Error as e: 
    print(f"Error: {e}")
    
# Close MariaDB connection
conn.close()
