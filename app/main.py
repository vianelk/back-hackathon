import pandas as pd
import mysql.connector

# Lire le fichier Excel
df = pd.read_excel("Presence_WiFi_Simulation.xlsx", engine='openpyxl')

# Connexion à MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpass",
    database="mydb"
)
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS presence_wifi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horodatage DATETIME,
    adresse_mac VARCHAR(17),
    carte_etudiant VARCHAR(50),
    statut VARCHAR(20),
    cours VARCHAR(50),
    salle VARCHAR(20),
    methode_detection VARCHAR(50),
    heure_fin TIME,
    geozone VARCHAR(50)
)
""")

# Insertion des données
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO presence_wifi (
            horodatage, adresse_mac, carte_etudiant, statut,
            cours, salle, methode_detection, heure_fin, geozone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        pd.to_datetime(row['Horodatage']),
        row['Adresse MAC'],
        row['Carte Étudiant'],
        row['Statut'],
        row['Cours'],
        row['Salle'],
        row['Méthode Détection'],
        pd.to_datetime(row['HeureFin']).time() if not pd.isna(row['HeureFin']) else None,
        row['Géozone']
    ))

conn.commit()
cursor.close()
conn.close()
