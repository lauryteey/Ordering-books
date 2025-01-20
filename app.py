from flask import Flask, jsonify, render_template, request, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Oppretter en Flask-applikasjon
app = Flask(__name__, template_folder="./Templates")
app.secret_key = 'Hei, secret key'  # En tilfeldig nøkkel som brukes for å kryptere sessions (brukerdata som lagres midlertidig).

# Kobler til en global MySQL-database
conn = mysql.connector.connect(
    host="localhost",         # Databasens adresse (lokal maskin)
    user="oppdrag_user",     # Brukernavnet til databasen.
    password="123",           # Passordet til databasen.
    database="oppdrag"       # Navnet på databasen som brukes.
)

# Oppretter en global cursor for å kjøre SQL-spørringer
cursor = conn.cursor(dictionary=True)  # Konfigurerer til å returnere resultater som dictionaries keys (nøkkel-verdi-par).

# Rute for innlogging
@app.route('/login', methods=['POST'])
def login():
    try:
        # Henter data som sendes i forespørselen (JSON-format).
        data = request.get_json()

        # Sjekker om nødvendige felter finnes i forespørselen.
        if 'e_post' not in data or 'passord' not in data:
            return jsonify({"error": "E-post og passord er påkrevd"}), 400

        e_post = data['e_post']  # Leser e-post fra forespørselen.
        passord = data['passord']  # Leser passord fra forespørselen.

        # SQL-statement, den sjekker om e-posten finnes i databasen.
        query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s" #%s placeholder for de ekte valuene
        cursor.execute(query, (e_post,)) #kjører query i datbasen bip bop
        user = cursor.fetchone()  # Henter resultatet fra databasen.

        if user:
            # Sjekker om passordet stemmer ved hjelp av hashing.
            if check_password_hash(user['passord'], passord):
                session['brukerID'] = user['brukerID']  # Lagre brukerID i session (midlertidig lagring).
                return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/main"}), 200
            else:
                return jsonify({"error": "Feil passord."}), 401
        else:
            return jsonify({"error": "Bruker ble ikke funnet."}), 404
    except mysql.connector.Error as e:
        # Feil relatert til databasen er her.
        print(f"Feil i databasen under login: {e}")
        return jsonify({"error": "En feil i databasen oppsto"}), 500
    except Exception as e:
        # Andre uventede feil håndteres her.
        print(f"Uforventet feil under login: {e}")
        return jsonify({"error": "Det skjedde en uventet feil"}), 500
    
# Rute for å opprette en ny bruker
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Henter data som sendes i forespørselen (JSON-format)
        data = request.get_json()

        # Sjekker om alle nødvendige felt er med i forespørselen
        if not all(key in data for key in ('e_post', 'passord', 'fornavn')):
            return jsonify({"error": "E-post, passord og navn er påkrevd"}), 400

        e_post = data['e_post']  # Henter e-post fra forespørselen
        passord = data['passord']  # Henter passord fra forespørselen
        fornavn = data['fornavn']  # Henter fornavn fra forespørselen

        # Sjekker om e-posten allerede finnes i databasen
        query = "SELECT e_post FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        if cursor.fetchone():
            return jsonify({"error": "E-posten er allerede registrert"}), 409

        # Genererer et hashed passord for sikker lagring
        hashed_passord = generate_password_hash(passord)

        # SQL-spørring for å legge til ny bruker
        query = """
            INSERT INTO bruker (e_post, passord, fornavn)
            VALUES (%s, %s, %s)
        """
        values = (e_post, hashed_passord, fornavn)
        cursor.execute(query, values)
        conn.commit()  # Lagrer endringene i databasen

        return jsonify({"message": "Brukeren ble opprettet!"}), 201
    except mysql.connector.Error as e:
        # Håndterer databasefeil
        print(f"Databasefeil under oppretting av bruker: {e}")
        return jsonify({"error": "En feil oppsto med databasen"}), 500
    except Exception as e:
        # Håndterer andre uventede feil
        print(f"Uventet feil under oppretting av bruker: {e}")
        return jsonify({"error": "Det oppsto en uventet feil"}), 500


@app.route('/sign_up')
def sign_up():
    return render_template('signUp.html')  

# Default route (Hjemmeside)
@app.route('/')
def home():
    # Viser innloggingssiden.
    return render_template('logIn.html')
