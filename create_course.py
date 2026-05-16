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

participants = [
    {"tnNr": "143", "name": "Schmidt, M.", "city": "Wedel"},
    {"tnNr": "145", "name": "Huber, Chr.", "city": "Augsburg"},
    {"tnNr": "146", "name": "Abele, I.", "city": "Ulm"},
    {"tnNr": "149", "name": "Kircher, B.", "city": "Augsburg"},
    {"tnNr": "155", "name": "Meier, W.", "city": "Muenchen"},
    {"tnNr": "171", "name": "Moeller, H.", "city": "Neusaess"},
    {"tnNr": "173", "name": "Schulze, B.", "city": "Krumbach"},
    {"tnNr": "177", "name": "Mons, F.", "city": "Donauwoerth"},
    {"tnNr": "185", "name": "Meier, K.", "city": "Landsberg"},
    {"tnNr": "187", "name": "Karstens, L.", "city": "Augsburg"},
    {"tnNr": "194", "name": "Gerstner, M.", "city": "Mindelheim"}
]

instructors = [
    {"persNr": "27183", "name": "Meier, I.", "gehalt": "4300.50"},
    {"persNr": "29594", "name": "Schulze, H.", "gehalt": "3890.20"},
    {"persNr": "38197", "name": "Huber, L.", "gehalt": "4200.10"},
    {"persNr": "43325", "name": "Mueller, K.", "gehalt": "3400.80"}
]

with GraphDatabase.driver(URI, auth=AUTH).session(database=DATABASE) as session:
    try:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("""
        UNWIND $courses AS course
        CREATE (c:Kurs)
        SET c = course
        """, courses=courses)
        session.run("""
        UNWIND $participants AS participant
        CREATE (p:Teilnehmer)
        SET p = participant
        """, participants=participants)
        session.run("""
        UNWIND $instructors as instructor
        CREATE(i:Kursleiter)
        SET i = instructor
        """, instructors=instructors)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
