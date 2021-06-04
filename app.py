from flask import Flask, render_template, request, session, redirect
from datetime import datetime, timedelta
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'SECRET_KEY'
app.permanent_session_lifetime = timedelta(minutes = 30)

def lancer():
    stream = open("AddToBDD.py")
    lu = stream.read()
    exec(lu)

@app.route('/')
def connexion():
    if request.remote_addr in session:
        return redirect('/index')
    else:
        return render_template('login.html')

@app.route('/auth/', methods=['POST'])
def auth():
    identifiant = request.form['Identifiant']
    mdp = request.form['mdp']
    conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute("SELECT password FROM connexion WHERE identifiant = '" + identifiant + "'")
    BDDmdp = cur.fetchone()
    cur.close()
    conn.close()
    if BDDmdp != None and bcrypt.check_password_hash(BDDmdp[0], mdp):
        session[request.remote_addr] = datetime.now()
        return redirect('/index')
    else:
        return redirect('/')

@app.route('/deconnexion')
def deco():
    session.pop(request.remote_addr, None)
    return redirect('/')

@app.route('/index')
def index():
    if(request.remote_addr in session ):
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("SELECT * FROM Etudiant")
        posts = cur.fetchall()
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")
        return render_template('dashboard.html', posts = posts)

    else:
        return redirect('/')  

@app.route('/ajouter')
def pageAjouter():
    if(request.remote_addr in session ):
        return render_template('ajouter.html')
    else:
        return redirect('/')

@app.route('/validation', methods=['POST'])
def ajouterEtRetour():
    if(request.remote_addr in session ):
        try :
            nom = request.form['nom']
            prenom = request.form['prenom']
            promo = request.form['promo']
            pic1 = request.files['photo1']
            pic2 = request.files['photo2']
            pic3 = request.files['photo3']
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
            conn.text_factory = str
            cur = conn.cursor()
            print("Connexion reussie à SQLite")
            cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Presence INT NOT NULL, Photo1 BLOB NOT NULL, Photo2 BLOB NOT NULL, Photo3 BLOB NOT NULL)")
            sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Presence, Photo1, Photo2, Photo3) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            print(pic1)
            print(pic2)
            print(pic3)
            blobFile1=pic1.read()
            blobFile2=pic2.read()
            blobFile3=pic3.read()
            value = (nom, prenom, promo, 0, blobFile1, blobFile2, blobFile3)
            cur.execute(sql, value)
            conn.commit()
            print("Fichier insere avec succes")
            cur.execute( "SELECT Nom, Prenom, Promo FROM Etudiant WHERE id =(SELECT MAX(id) FROM Etudiant)")
            validation = cur.fetchone()
            print(validation[0])
            print(validation[1])
            print(validation[2])
            cur.close()
            conn.close()
            print("Connexion SQLite est fermee")

        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)

        return render_template('valid.html', validation = validation)

    else:
        return redirect('/')


@app.route("/ajouterCO")
def ajouterCo():
    return render_template("ajouterCo.html")

@app.route('/validCo', methods=['POST'])
def ajouterIdentifiant():
    try :
        identifiant = request.form['identifiant']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password)
        print(identifiant)
        print(pw_hash)
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="b8523d276180fb", password="e548c5fe", database="heroku_432d5a7d6f44b44")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        sql = "INSERT INTO connexion (identifiant, password) VALUES (%s,%s)"
        value = (identifiant, pw_hash)
        cur.execute(sql, value)
        conn.commit()
        print("Fichier insere avec succes")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")

    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion", error)
        
    return render_template("validation.html")