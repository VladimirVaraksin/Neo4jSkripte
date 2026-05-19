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
        CREATE CONSTRAINT kurs_kursNr IF NOT EXISTS
        FOR (k:Kurs)
        REQUIRE k.kursNr IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT teilnehmer_tnNr IF NOT EXISTS
        FOR (t:Teilnehmer)
        REQUIRE t.tnNr IS UNIQUE
        """)

        session.run("""
        CREATE CONSTRAINT kursleiter_persNr IF NOT EXISTS
        FOR (kl:Kursleiter)
        REQUIRE kl.persNr IS UNIQUE
        """)

        indexes = session.run("SHOW INDEXES")
        print_records("Indexes", indexes)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
