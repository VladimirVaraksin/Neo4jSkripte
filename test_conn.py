import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

def test_connection():
    if not all([URI, AUTH[0], AUTH[1]]):
        print("Fehler: Umgebungsvariablen unvollständig.")
        return
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("Verbindung erfolgreich.")

if __name__ == "__main__":
    test_connection()
