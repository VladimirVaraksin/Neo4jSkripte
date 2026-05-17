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
        places = session.run("""
        MATCH (:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)
        RETURN a.ort
        """)
        print_records("Alle Orte, an denen Kurse durchgeführt werden.", places)

        participants_augs = session.run("""
        MATCH (t:Teilnehmer)
        WHERE t.ort = 'Augsburg'
        RETURN t
        """)
        print_records("Alle Teilnehmer in Augsburg.", participants_augs)

        instructors = session.run("""
        MATCH(kl:Kursleiter)
        WHERE kl.gehalt >= 3000 AND kl.gehalt <= 4000
        ORDER BY kl.name
        RETURN kl
        """)
        print_records("Alle Kursleiter mit einem Gehalt zw. 3000 und 4000 sortiert nach Namen.", instructors)

        course_titles = session.run("""
        MATCH (k:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)
        RETURN k.titel, a.datum, a.ort
        """)
        print_records("die Kurstitel mit Datum und Ort, an dem sie stattfinden.", course_titles)

        course_titles_with_instructors = session.run("""
        MATCH (k:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)<-[:FUEHRT]-(kl:Kursleiter)
        RETURN k.titel, a.datum, a.ort, kl.name
        """)
        print_records("die Kurstitel mit Datum und Ort, an dem sie stattfinden und Kursleiter.", course_titles_with_instructors)

        requirements = session.run("""
        MATCH (k:Kurs) 
        OPTIONAL MATCH (k)-[:VORAUSSETZUNG]->(v:Kurs)
        RETURN k.titel AS Kurstitel, v.titel AS Voraussetzung
        """)
        print_records("Voraussetzungen", requirements)

    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
