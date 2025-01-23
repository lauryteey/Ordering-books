from flask import Flask, jsonify, render_template, request, session
import mysql.connector
import re
from werkzeug.security import generate_password_hash, check_password_hash

# Lager en Flask-applikasjon
app = Flask(__name__, template_folder="./templates")
app.secret_key = 'Hei, secret key'  # En tilfeldig nøkkel som brukes for å kryptere brukerdata (sessions).

# Kobler til en MySQL-database
conn = mysql.connector.connect(
    host="10.0.0.19",         # IP-adressen til databasen (her er det en lokal maskin).
    user="oppdrag_user",     # Brukernavnet som brukes til å koble til databasen.
    password="123",           # Passordet til databasen.
    database="oppdrag"       # Navnet på databasen som brukes
)

# Lager en cursor som kan brukes til å sende SQL-spørringer til databasen
cursor = conn.cursor(dictionary=True)  # Gir resultatene som dictionaries (nøkkel-verdi-par).


# Rute for innlogging
@app.route('/login', methods=['POST'])
def login():
    try:
        # Henter data som sendes med i forespørselen (i JSON-format).
        data = request.get_json()

        # Sjekker at både e-post og passord er med i forespørselen.
        if 'e_post' not in data or 'passord' not in data:
            return jsonify({"error": "E-post og passord er påkrevd"}), 400

        e_post = data['e_post']  # Henter e-post fra dataene.
        passord = data['passord']  # Henter passord fra dataene.

        # Sjekker om e-posten finnes i databasen.
        query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))  # Kjører spørringen i databasen.
        user = cursor.fetchone()  # Henter resultatet (én bruker).

        if user:
            # Sjekker om passordet stemmer med det lagrede passordet.
            if check_password_hash(user['passord'], passord):
                session['brukerID'] = user['brukerID']  # Lagre brukerens ID i session (midlertidig lagring).
                return jsonify({"message": "Klarte å logge inn!", "redirect": "/bestilling"}), 200
            else:
                return jsonify({"error": "Feil passord."}), 401
        else:
            return jsonify({"error": "Bruker ble ikke funnet."}), 404
    except mysql.connector.Error as e:
        # Hvis det er en feil med databasen.
        print(f"Feil i databasen under login: {e}")
        return jsonify({"error": "En feil i databasen oppsto"}), 500
    except Exception as e:
        # Hvis det er en annen feil som ikke er relatert til databasen.
        print(f"Uforventet feil under login: {e}")
        return jsonify({"error": "Det skjedde en uventet feil"}), 500
    

# Rute for å opprette en ny bruker
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Henter data som sendes med i forespørselen (i JSON-format)
        data = request.get_json()

        # Sjekker om nødvendige felter er med i forespørselen
        if not all(key in data for key in ('e_post', 'passord', 'fornavn')):
            return jsonify({"error": "E-post, passord og navn er påkrevd"}), 400

        e_post = data['e_post'].strip()  # Henter e-post fra dataene
        passord = data['passord'].strip()  # Henter passord fra dataene
        fornavn = data['fornavn'].strip()  # Henter fornavn fra dataene
        
        # Sjekker om passordet er sterkt nok
        if not er_passord_sikkert(passord):
            return jsonify({"error": "Passordet må være minst 8 tegn, med store og små bokstaver, tall og spesialtegn."}), 400

        # Sjekker om e-posten allerede finnes i databasen
        query = "SELECT e_post FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        if cursor.fetchone():
            return jsonify({"error": "E-posten er allerede registrert"}), 409

        # Lager et hashet passord for sikker lagring
        hashed_passord = generate_password_hash(passord)

        # SQL-spørring for å legge til ny bruker i databasen
        query = """
            INSERT INTO bruker (e_post, passord, fornavn)
            VALUES (%s, %s, %s)
        """
        values = (e_post, hashed_passord, fornavn)
        cursor.execute(query, values)
        conn.commit()  # Lagrer endringene i databasen

        return jsonify({"message": "Brukeren ble opprettet!"}), 201
    except mysql.connector.Error as e:
        # Feil i databasen når vi prøver å opprette en bruker
        print(f"Databasefeil under oppretting av bruker: {e}")
        return jsonify({"error": "En feil oppsto med databasen"}), 500
    except Exception as e:
        # Uventede feil håndteres her
        print(f"Uventet feil under oppretting av bruker: {e}")
        return jsonify({"error": "Det oppsto en uventet feil"}), 500
    

@app.route('/bestilling', methods=['POST'])
def sende_bestilling():
    try:
        # Sjekker om brukeren er logget inn.
        if 'brukerID' not in session:
            return jsonify({'error': 'Bruker er ikke logget inn'}), 401

        data = request.get_json()  # Henter data fra forespørselen
        print(f"Mottatt data: {data}")  # Debugger for å vise dataene som ble sendt

        translate_from = data['translate_from'].strip()  # Henter språket du oversetter fra
        translate_to = data['translate_to'].strip()  # Henter språket du oversetter til
        delivery_time = data['delivery_time']  # Henter leveringstiden
        description = data['description'].strip()  # Henter beskrivelsen av oppdraget

        # Sjekker at alle nødvendige felt er fylt ut
        if not translate_from or not translate_to or not description or not delivery_time:
            return jsonify({'error': 'Alle feltene er påkrevd'}), 400
        if len(translate_from) > 50 or len(translate_to) > 50:
            return jsonify({'error': 'Språkfeltene må være maks 50 tegn'}), 400
        if len(description) > 500:
            return jsonify({'error': 'Beskrivelsen kan maks være 500 tegn'}), 400

        brukerID = session['brukerID']  # Henter brukerID fra session

        # Legger inn bestillingen i databasen
        query = """
            INSERT INTO arbeid_bestilling (brukerID, BESKRIVELSE, oversett_fra, oversett_til, leveringstid)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (brukerID, description, translate_from, translate_to, delivery_time)

        cursor.execute(query, values)  # Kjører SQL-spørringen
        print(f"Query kjørt med verdier: {values}")  # Debug
        conn.commit()  # Lagrer endringen i databasen

        return jsonify({"message": "Bestillingen ble sendt!"}), 201

    except mysql.connector.Error as e:
        # Håndterer eventuelle databasefeil
        print(f"Databasefeil: {e}", exc_info=True)
        return jsonify({"error": "En feil oppsto med databasen"}), 500
    except Exception as e:
        # Håndterer uventede feil
        print(f"Uventet feil: {e}", exc_info=True)
        return jsonify({"error": "Det oppsto en uventet feil"}), 500


# Funksjon for å validere at passordet er sterkt nok
def er_passord_sikkert(password):
    """
    Sjekker at passordet møter sikkerhetskravene:
    - Minst 8 tegn langt
    - Må ha minst én stor bokstav
    - Må ha minst én liten bokstav
    - Må ha minst ett tall
    - Må ha minst ett spesialtegn
    """
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(password_regex, password)

@app.route('/sign_up')
def sign_up():
    # Viser registreringssiden
    return render_template('Signup.html')  

# Hjemmesiden
@app.route('/')
def home():
    # Viser innloggingssiden
    return render_template('Login.html')

@app.route('/bestilling')
def bestilling():
    # Viser bestillingssiden
    return render_template('bestillinger.html')

@app.route('/bekreftelse')
def bekreftelse():
    # Viser bekreftelsessiden
    return render_template('confirmPage.html')


# Starter Flask-applikasjonen
if __name__ == '__main__':
    try:
        app.run(debug=True)  # Kjører appen i debug-modus for å se feil
    except Exception as e:
        
        print(f"Feilet når Flask-appen ble startet: {e}")
