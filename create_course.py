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
    {"tnNr": 143, "name": "Schmidt, M.", "ort": "Wedel"},
    {"tnNr": 145, "name": "Huber, Chr.", "ort": "Augsburg"},
    {"tnNr": 146, "name": "Abele, I.", "ort": "Ulm"},
    {"tnNr": 149, "name": "Kircher, B.", "ort": "Augsburg"},
    {"tnNr": 155, "name": "Meier, W.", "ort": "Muenchen"},
    {"tnNr": 171, "name": "Moeller, H.", "ort": "Neusaess"},
    {"tnNr": 173, "name": "Schulze, B.", "ort": "Krumbach"},
    {"tnNr": 177, "name": "Mons, F.", "ort": "Donauwoerth"},
    {"tnNr": 185, "name": "Meier, K.", "ort": "Landsberg"},
    {"tnNr": 187, "name": "Karstens, L.", "ort": "Augsburg"},
    {"tnNr": 194, "name": "Gerstner, M.", "ort": "Mindelheim"}
]

instructors = [
    {"persNr": 27183, "name": "Meier, I.", "gehalt": 4300.50},
    {"persNr": 29594, "name": "Schulze, H.", "gehalt": 3890.20},
    {"persNr": 38197, "name": "Huber, L.", "gehalt": 4200.10},
    {"persNr": 43325, "name": "Mueller, K.", "gehalt": 3400.80}
]

offers = [
    {"angNr": 1, "kursNr": "G08", "datum": "2023-10-13", "ort": "Wedel"},
    {"angNr": 2, "kursNr": "G08", "datum": "2023-11-24", "ort": "Ulm"},
    {"angNr": 1, "kursNr": "G10", "datum": "2023-12-01", "ort": "Augsburg"},
    {"angNr": 2, "kursNr": "G10", "datum": "2023-02-15", "ort": "Muenchen"},
    {"angNr": 1, "kursNr": "P13", "datum": "2023-05-28", "ort": "Augsburg"},
    {"angNr": 2, "kursNr": "P13", "datum": "2023-07-01", "ort": "Augsburg"},
    {"angNr": 1, "kursNr": "I09", "datum": "2023-03-27", "ort": "Mindelheim"},
    {"angNr": 2, "kursNr": "I09", "datum": "2023-04-23", "ort": "Muenchen"},
    {"angNr": 3, "kursNr": "I09", "datum": "2023-05-29", "ort": "Ulm"}
]

requirements = [
    {"vorNr": "G08", "kursNr": "P13"},
    {"vorNr": "G10", "kursNr": "P13"},
    {"vorNr": "G08", "kursNr": "I09"},
    {"vorNr": "G10", "kursNr": "I09"},
    {"vorNr": "P13", "kursNr": "I09"}
]

takes_part = [
    {"angNr": 2, "kursNr": "G08", "tnNr": 143},
    {"angNr": 2, "kursNr": "P13", "tnNr": 143},
    {"angNr": 1, "kursNr": "G08", "tnNr": 145},
    {"angNr": 1, "kursNr": "P13", "tnNr": 146},
    {"angNr": 1, "kursNr": "I09", "tnNr": 146},
    {"angNr": 2, "kursNr": "P13", "tnNr": 149},
    {"angNr": 1, "kursNr": "I09", "tnNr": 155},
    {"angNr": 1, "kursNr": "I09", "tnNr": 171},
    {"angNr": 1, "kursNr": "I09", "tnNr": 173},
    {"angNr": 2, "kursNr": "P13", "tnNr": 177},
    {"angNr": 1, "kursNr": "I09", "tnNr": 185},
    {"angNr": 2, "kursNr": "I09", "tnNr": 187},
    {"angNr": 1, "kursNr": "P13", "tnNr": 194}
]

instructed_by = [
    {"angNr": 1, "kursNr": "G08", "persNr": 38197},
    {"angNr": 2, "kursNr": "G08", "persNr": 38197},
    {"angNr": 1, "kursNr": "G10", "persNr": 43325},
    {"angNr": 2, "kursNr": "G10", "persNr": 29594},
    {"angNr": 1, "kursNr": "P13", "persNr": 27183},
    {"angNr": 2, "kursNr": "P13", "persNr": 27183},
    {"angNr": 1, "kursNr": "I09", "persNr": 29594},
    {"angNr": 2, "kursNr": "I09", "persNr": 29594},
    {"angNr": 3, "kursNr": "I09", "persNr": 29594}
]

fees = [
    {"angNr": 2, "kursNr": "G08", "tnNr": 143, "gebuehr": 500},
    {"angNr": 2, "kursNr": "P13", "tnNr": 143, "gebuehr": 400},
    {"angNr": 1, "kursNr": "G08", "tnNr": 145, "gebuehr": None},
    {"angNr": 1, "kursNr": "P13", "tnNr": 146, "gebuehr": 300},
    {"angNr": 1, "kursNr": "I09", "tnNr": 146, "gebuehr": None},
    {"angNr": 2, "kursNr": "P13", "tnNr": 149, "gebuehr": 350},
    {"angNr": 1, "kursNr": "I09", "tnNr": 155, "gebuehr": None},
    {"angNr": 1, "kursNr": "I09", "tnNr": 171, "gebuehr": None},
    {"angNr": 1, "kursNr": "I09", "tnNr": 173, "gebuehr": 400},
    {"angNr": 2, "kursNr": "P13", "tnNr": 177, "gebuehr": None},
    {"angNr": 1, "kursNr": "I09", "tnNr": 185, "gebuehr": 450},
    {"angNr": 2, "kursNr": "I09", "tnNr": 187, "gebuehr": None},
    {"angNr": 1, "kursNr": "P13", "tnNr": 194, "gebuehr": None}
]

literature = [
    {"kursNr": "G08", "bestand": 4, "bedarf": 2, "preis": 10.50},
    {"kursNr": "I09", "bestand": 2, "bedarf": 6, "preis": 8.00},
    {"kursNr": "P13", "bestand": 3, "bedarf": 5, "preis": 15.20}
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
        
        session.run("""
        UNWIND $offers as offer
        MATCH (k:Kurs {kursNr: offer.kursNr})
        CREATE(o:Angebot {angNr: offer.angNr})
        SET o.datum = date(offer.datum),
        o.ort = offer.ort
        CREATE (k)-[:ANGEBOTEN_ALS]->(o)
        """, offers=offers)

        session.run("""
        UNWIND $requirements as requirement
        MATCH (k:Kurs {kursNr: requirement.kursNr})
        MATCH (v:Kurs {kursNr: requirement.vorNr})
        CREATE (k)-[:VORAUSSETZUNG]->(v)
        """, requirements=requirements)

        session.run("""
        UNWIND $takes_part as tp
        MATCH (k:Kurs {kursNr: tp.kursNr})-[:ANGEBOTEN_ALS]->(a:Angebot {angNr: tp.angNr})
        MATCH (t:Teilnehmer {tnNr: tp.tnNr})
        CREATE (t)-[:NIMMT_TEIL]->(a)
        """, takes_part=takes_part)

        session.run("""
        UNWIND $instructed_by as ib
        MATCH (k:Kurs {kursNr: ib.kursNr})-[:ANGEBOTEN_ALS]->(a:Angebot {angNr: ib.angNr}) 
        MATCH(p:Kursleiter {persNr: ib.persNr})
        CREATE (p)-[:FUEHRT]->(a)
        """, instructed_by=instructed_by)

        session.run("""
        UNWIND $fees as fee
        MATCH (k:Kurs {kursNr: fee.kursNr})-[:ANGEBOTEN_ALS]->(a:Angebot {angNr: fee.angNr})
        MATCH (t:Teilnehmer {tnNr: fee.tnNr})
        CREATE (t)-[r:GEBUEHREN]->(a)
        SET r.gebuehr = fee.gebuehr
        """, fees=fees)

        session.run("""
        UNWIND $literature AS lit
        MATCH (k:Kurs {kursNr: lit.kursNr})
        CREATE (kl:Kursliteratur {bestand: lit.bestand, bedarf: lit.bedarf, preis: lit.preis})
        CREATE (k)-[:VERWENDET_LITERATUR]->(kl)
        """, literature=literature)
    except Neo4jError as e:
        print('Exception GQL status:', e.gql_status)
        print('Exception GQL status description:', e.gql_status_description)
        print('Exception GQL cause:', e.__cause__)
