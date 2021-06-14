from flask import Flask, render_template, request, session, redirect
from datetime import datetime, timedelta
import mysql.connector
from flask_bcrypt import Bcrypt
from PIL import Image
import math

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'SECRET_KEY'
app.permanent_session_lifetime = timedelta(minutes = 30)


#si on veut en local on change  request.headers.get("X-Forwarded-For") par request.remote_addr

@app.route('/')
def connexion():
    remote_addr = request.headers.get("X-Forwarded-For")
    print("C'EST LA")
    print(remote_addr)
    #print(request.environ['REMOTE_ADDR'])
    print(request.headers.get("X-Forwarded-For"))
    if (request.headers.get("X-Forwarded-For") in session):
        return redirect('/index')
    else:
        return render_template('login.html')

@app.route('/auth/', methods=['POST'])
def auth():
    identifiant = request.form['Identifiant']
    mdp = request.form['mdp']
    conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute("SELECT password FROM connexion WHERE identifiant = '" + identifiant + "'")
    BDDmdp = cur.fetchone()
    cur.close()
    conn.close()
    if BDDmdp != None and bcrypt.check_password_hash(BDDmdp[0], mdp):
        print("IF")
        session[request.headers.get("X-Forwarded-For")] = identifiant
        return redirect('/index')
    else:
        print("ELSE")
        return redirect('/')

@app.route('/deconnexion')
def deco():
    session.pop(request.headers.get("X-Forwarded-For"), None)
    return redirect('/')

@app.route('/index')
def index():
    if(request.headers.get("X-Forwarded-For") in session ):
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Presence VARCHAR(45) NOT NULL, Photo1 BLOB NOT NULL, Photo2 BLOB NOT NULL, Photo3 BLOB NOT NULL, Photo4 BLOB NOT NULL, Photo5 BLOB NOT NULL, Photo6 BLOB NOT NULL, Photo7 BLOB NOT NULL)")
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
    if(request.headers.get("X-Forwarded-For") in session ):
        return render_template('ajouter.html')
    else:
        return redirect('/')

@app.route('/validation', methods=['POST'])
def ajouterEtRetour():
    if(request.headers.get("X-Forwarded-For") in session ):
        try :
            nom = request.form['nom']
            prenom = request.form['prenom']
            promo = request.form['promo']
            pic1 = request.files['photo1']
            pic2 = request.files['photo2']
            pic3 = request.files['photo3']
            pic4 = request.files['photo4']
            pic5 = request.files['photo5']
            pic6 = request.files['photo6']
            pic7 = request.files['photo7']
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            print("Connexion reussie à SQLite")
            sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Presence, Photo1, Photo2, Photo3, Photo4, Photo5, Photo6, Photo7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            blobFile1 = pic1.read()
            blobFile2 = pic2.read()
            blobFile3 = pic3.read()
            blobFile4 = pic4.read()
            blobFile5 = pic5.read()
            blobFile6 = pic6.read()
            blobFile7 = pic7.read()
            cur.execute("SELECT * FROM etudiant WHERE Nom LIKE '" + nom + "%' AND Prenom LIKE '" + prenom + "%'")
            long = len(cur.fetchall())
            print(len(cur.fetchall()))
            if long > 0:
                nom = nom + str(long)
                prenom = prenom + str(long)
            value = (nom, prenom, promo, '$', blobFile1, blobFile2, blobFile3, blobFile4, blobFile5, blobFile6, blobFile7)
            cur.execute(sql, value)
            conn.commit()
            print("Fichier insere avec succes")
            cur.execute( "SELECT Nom, Prenom, Promo FROM Etudiant WHERE id = (SELECT MAX(id) FROM Etudiant)")
            validation = cur.fetchone()
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
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        sql = "INSERT INTO connexion (Identifiant, Password) VALUES (%s,%s)"
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

@app.route('/annee', methods=['POST'])
def annee():
    if(request.headers.get("X-Forwarded-For") in session ):
        try:
            annee = request.form['annee']
            annees = []
            annees.append(annee)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            print("Connexion reussie à SQLite")
            if annees[0] == '4':
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'M1')")

            elif annees[0] == '5':
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'M2')")

            else :
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'CIR" + annee + "' OR Promo = 'CPG" + annee + "' OR Promo = 'CNB" + annee + "')")
            posts = cur.fetchall()
            return render_template('annee.html', posts = posts, annee = annees)
        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)
    else:
        return redirect('/')
    
    

@app.route('/promo', methods=['POST'])
def promo():
    try :
        if(request.headers.get("X-Forwarded-For") in session ):
            promo = request.form['promo']
            promos = []
            promos.append(promo)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            print("Connexion reussie à SQLite")
            cur.execute("SELECT * FROM Etudiant WHERE (Promo = '" + promo + "')")
            posts = cur.fetchall()
            return render_template('promo.html', posts = posts, promo = promos)

        else:
            return redirect('/')
    
    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion", error)

@app.route('/graphes')
def graphes():
    if(request.headers.get("X-Forwarded-For") in session ):
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
        conn.text_factory = str
        cur = conn.cursor()
        print("Connexion reussie à SQLite")
        cur.execute("SELECT * FROM Etudiant")
        posts = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM Etudiant WHERE Presence = '%'")
        presences = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Etudiant WHERE Presence = '$'")
        absences = cur.fetchone()[0]
        cur.close()
        conn.close()
        print("Connexion SQLite est fermee")
        try:
            pctPre = round(presences/(presences + absences) * 100, 2)
            pctAbs = round(absences/(presences + absences) * 100, 2)
            pct = []
            pct.append(pctPre)
            pct.append(pctAbs)
            return render_template('graphes.html', posts = posts, presences = presences, absences = absences, pct = pct)
        except:
            print("error")
            return redirect('/index') 


    else:
        return redirect('/') 

@app.route('/supprimer')
def pageSupprimer():
    if (request.headers.get("X-Forwarded-For") in session) :
        return render_template('supprimer.html')
    else:
        return redirect('/')

@app.route('/validSupr', methods=['POST'])
def supprimer():
    if (request.headers.get("X-Forwarded-For") in session) :
        validations=[]
        try :
            nom = request.form['nom']
            prenom = request.form['prenom']
            promo = request.form['promo']
            print(nom)
            print(prenom)
            print(promo)
            validations.append(nom)
            validations.append(prenom)
            validations.append(promo)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            print("Connexion reussie à SQLite")
            cur.execute("SELECT id FROM etudiant WHERE Nom = '" + nom + "' AND Prenom = '" + prenom + "' AND Promo = '" + promo + "'")
            id = cur.fetchone()
            if(id!=None):
                print(id[0])
                idstr = str(id[0])
                cur.execute("DELETE FROM etudiant WHERE id = '" + idstr + "'")
                conn.commit()
                print("Fichier supprimé avec succes")
                cur.close()
                conn.close()
                print("Connexion SQLite est fermee")
            else:
                cur.close()
                conn.close()
                print("Connexion SQLite est fermee")
                return render_template('IncorrectSuppr.html')

        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)

        return render_template('validSupr.html',validations=validations)

    else:
        return redirect('/') 

@app.route('/settings')
def settings():
    if(request.headers.get("X-Forwarded-For")  in session):
        return render_template('settings.html')
    else:
        return redirect('/')

@app.route('/newMDP', methods=['POST'])
def newMDP():
    if(request.headers.get("X-Forwarded-For")  in session):
        try:
            print("ON EST LA 1")
            identifiant = request.form['identifiant']
            if(identifiant == session[request.headers.get("X-Forwarded-For")]):
                print("ON EST LA2")
                ancienMDP = request.form['ancienMDP']
                nouveauMDP = request.form['nouveauMDP']
                conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
                conn.text_factory = str
                cur = conn.cursor()
                print("Connexion reussie à SQLite")
                cur.execute("SELECT Password FROM connexion WHERE Identifiant = '" + identifiant + "'")
                password = cur.fetchone()
                print(password)
                if(bcrypt.check_password_hash(password[0], ancienMDP)):
                    print("ON EST LA3")
                    pw_hash = bcrypt.generate_password_hash(nouveauMDP)
                    print('verif')
                    cur.execute("DELETE FROM connexion WHERE Identifiant = '" + identifiant + "'")
                    conn.commit()
                    sql = "INSERT INTO connexion (Identifiant, Password) VALUES (%s,%s)"
                    value = (identifiant, pw_hash)
                    cur.execute(sql, value)
                    conn.commit()
                    
                else:
                    return redirect('/settings')
                cur.close()
                conn.close()
                print("Connexion SQLite est fermee")
                return redirect('/index')
            return redirect('/settings')
        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)
    else:
        return redirect('/')