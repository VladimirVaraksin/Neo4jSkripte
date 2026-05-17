import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError
from print_record import print_records

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
DATABASE = (os.getenv("NEO4J_DATABASE"))

with GraphDatabase.driver(URI, auth=AUTH).session(database=DATABASE) as session:
    try:
        session.run("""
        MATCH (a:Angebot)
        WHERE a.datum < date({year: 2024})
        SET a.datum = CASE 
        WHEN a.datum.month = 2 AND a.datum.day = 29
        THEN date({year: 2026, month: 2, day: 28})
        ELSE date({year: 2026, month: a.datum.month, day: a.datum.day})
        END
        """)
       
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
