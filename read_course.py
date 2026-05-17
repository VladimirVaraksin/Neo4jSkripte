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

        participants_own_place = session.run("""
        MATCH (t:Teilnehmer)-[:NIMMT_TEIL]->(a:Angebot)
        WHERE t.ort = a.ort
        RETURN t
        """)
        print_records("alle Teilnehmer, die einen Kurs am eigenen Wohnort gebucht haben.", participants_own_place)

        offers_without_participants = session.run("""
        OPTIONAL MATCH (t:Teilnehmer)-[:NIMMT_TEIL]->(:Angebot)<-[:ANGEBOTEN_ALS]-(k:Kurs)
        WITH k, count(t) as anz_tn
        WHERE anz_tn = 0
        MATCH (k)-[:ANGEBOTEN_ALS]->(a:Angebot)
        RETURN k.titel AS Titel, a.angNr AS Angebotsnummer
        """)
        print_records("alle Kursangebote (Kurstitel und Angebotsnummer), zu denen es noch keine Teilnehmer gibt", offers_without_participants)

        courses_with_more_two_pp = session.run("""
        MATCH (t:Teilnehmer)-[:NIMMT_TEIL]->(:Angebot)<-[:ANGEBOTEN_ALS]-(k:Kurs)
        WITH k, count(t) as anz_tn
        WHERE anz_tn > 2
        RETURN k
        """)
        print_records("Alle Kurse mit mindestens 2 Teilnehmern", courses_with_more_two_pp)
        
        all_meier = session.run("""
        OPTIONAL MATCH (t:Teilnehmer)
        WHERE toLower(t.name) CONTAINS "meier"
        OPTIONAL MATCH (l:Kursleiter)
        WHERE toLower(l.name) CONTAINS "meier"
        WITH collect(distinct t) AS teilnehmer, collect(distinct l) AS kursleiter
        RETURN teilnehmer + kursleiter AS personen
        """)
        print_records("alle Meier, sowohl Teilnehmer wie auch Kursleiter.", all_meier)

        course_num_offers = session.run("""
        OPTIONAL MATCH (k:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)
        WITH k.titel AS Titel, count(a) AS Anzahl_Angebote
        RETURN Titel, Anzahl_Angebote
        """)
        print_records("die Kurstitel mit der jeweiligen Anzahl der Angebote.", course_num_offers)

        course_requirements = session.run("""
        MATCH (k:Kurs)-[:VORAUSSETZUNG]->(v:Kurs)
        WITH k.titel AS Titel, count(v) AS anz_vorauss
        WHERE anz_vorauss >= 2
        ORDER BY anz_vorauss DESC
        RETURN Titel, anz_vorauss
        """)
        print_records("""die Kurstitel mit der Anzahl der Voraussetzungen, die mindestens 2 Voraussetzungen haben.
        Die Ausgabe soll so erfolgen, dass die Kurse mit
        den meisten Voraussetzungen zuerst kommen.""", course_requirements)


        course_instructors = session.run("""
        MATCH (k:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)<-[:FUEHRT]-(l:Kursleiter)
        WITH k.titel AS Titel, avg(l.gehalt) AS avg_gehalt
        RETURN Titel, avg_gehalt
        """)
        print_records("""Für alle Kurse (Titel ausgeben) das durchschnittliche Gehalt der Kursleiter,
        die ein Angebot dieses Kurses durchführen (nach diesem Durchschnitt aufsteigend sortiert).""", course_instructors)

        instructor_pairs = session.run("""
        MATCH (k:Kurs)-[:ANGEBOTEN_ALS]->(a:Angebot)<-[:FUEHRT]-(l:Kursleiter)
        RETURN k.titel, collect(distinct l.name) as kursleiter
        """)
        print_records("""alle Paare von Kursleitern, die denselben Kurs halten, und den entsprechenden Kurstitel""",
                      instructor_pairs)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
