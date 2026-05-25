import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
DATABASE = (os.getenv("NEO4J_DATABASE"))

with GraphDatabase.driver(URI, auth=AUTH).session(database=DATABASE) as session:
    try:
        session.run("""
        MATCH (:Kurs {titel: "C-Programmierung"})-[:VERWENDET_LITERATUR]->(kl:Kursliteratur)
        DETACH DELETE kl
        """)
        
        session.run("""
        MATCH (k:Kurs)
        OPTIONAL MATCH (t:Teilnehmer)-[:NIMMT_TEIL]->(:Angebot)<-[:ANGEBOTEN_ALS]-(k)
        WITH k, count(t) as anz_tn
        WHERE anz_tn < 2
        OPTIONAL MATCH (k)-[:VERWENDET_LITERATUR]->(l:Kursliteratur)
        OPTIONAL MATCH (k)-[:ANGEBOTEN_ALS]->(a:Angebot)
        DETACH DELETE k, a, l
        """)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
