import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
DATABASE = (os.getenv("NEO4J_DATABASE"))

courses = [{"kursNr": "G08", "titel": "Grundlagen I"},
           {"kursNr": "G10", "titel": "Grundlagen II"},
           {"kursNr": "P13", "titel": "C-Programmierung"},
           {"kursNr": "I09", "titel": "Datenbanken"}]

with GraphDatabase.driver(URI, auth=AUTH).session(database=DATABASE) as session:
    try:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("""
        UNWIND $courses AS course
        CREATE (c:Kurs)
        SET c = course
        """, courses=courses)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
