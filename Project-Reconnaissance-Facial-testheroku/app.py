from flask import Flask, render_template, request, session, redirect
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.permanent_session_lifetime = timedelta(minutes = 1)



def lancer():
    stream = open("AddToBDD.py")
    lu = stream.read()
    exec(lu)

@app.route('/')
def connexion():
    if request.remote_addr in session:
        return redirect('/BDD')
    else:
        return render_template('connexion.html')

@app.route('/auth/', methods=['POST'])
def auth():
    identifiant = request.form['Identifiant']
    mdp = request.form['mdp']
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="test")
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute("SELECT MDP FROM test.identifiant WHERE identifiant = '" + identifiant + "'")
    BDDmdp = cur.fetchall()
    cur.close()
    conn.close()
    if mdp == BDDmdp[0][0]:
        session[request.remote_addr] = datetime.now()
        return redirect('/BDD')
    else:
        return redirect('/')

@app.route('/deconnexion')
def deco():
    session.pop(request.remote_addr, None)
    return redirect('/')

@app.route('/ajouter/')
def pageAjouter():
    if request.remote_addr in session:
        return render_template('ajouter.html')
    else:
        return redirect('/')

@app.route('/BDD')
def BDD():
    if request.remote_addr in session:
        print("je suis la ")
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="test")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("SELECT * FROM Etudiant")
        posts=cur.fetchall()
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")
        return render_template('pageBDD.html',posts=posts)
    else:
        return redirect('/')

@app.route('/index/', methods=['POST'])
def ajouterEtRetour():
    nom = request.form['nom']
    prenom = request.form['prenom']
    promo = request.form['promo']
    pic1=request.files['photo1']
    pic2=request.files['photo2']
    pic3=request.files['photo3']
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="test")
    conn.text_factory = str
    cur = conn.cursor()
    print("Connexion reussie à SQLite")
    cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Etat INT NOT NULL, Photo1 BLOB NOT NULL,Photo2 BLOB NOT NULL,Photo3 BLOB NOT NULL)")
    sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Etat, Photo1,Photo2,Photo3) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    print(pic1)
    print(pic2)
    print(pic3)
    blobFile1=pic1.read()
    blobFile2=pic2.read()
    blobFile3=pic3.read()
    value = (nom, prenom, promo, 0, blobFile1,blobFile2,blobFile3)
    cur.execute(sql, value)
    conn.commit()
    print("Fichier insere avec succes")
    cur.close()
    conn.close()
    print("Connexion SQLite est fermee")
    return redirect('/BDD')