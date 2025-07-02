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
