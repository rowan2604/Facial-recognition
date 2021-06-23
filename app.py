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
    if (request.headers.get("X-Forwarded-For") in session): # On vérifie si on a déjà une session ouverte
        return redirect('/index')# Si on est déjà connecté on ouvre directement la page index
    else:
        return render_template('login.html')# Sinon on lance la page de connexion au site

# Page servant à vérifier si la combinaison identifiant/mot de passe coïncident bien avec une déjà présente dans la BDD
@app.route('/auth/', methods=['POST'])
def authentification():
     # On réupère les différentes valeurs entré dans les champs de noter formulaire
    identifiant = request.form['Identifiant']
    mdp = request.form['mdp']
    # On se connecte ensuite à notre BDD en renseigannt toutes les information nécessaires
    conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
    conn.text_factory = str # On définit notre connexion à la BDD comme un type string
    cur = conn.cursor()#On crée un curseur qui nous servira à effectuer toutes les requêtes SQL nécessaires
    cur.execute("SELECT password FROM connexion WHERE identifiant = '" + identifiant + "'") # On récupère alors le mot de passe qui correspond à l'identifiant rentré dans notre formulaire
    BDDmdp = cur.fetchone()# On stocke le mot de passe dans une variable de type tableau
    cur.close()# On ferme le curseur 
    conn.close()# On ferme la connexion
    #On vérifie que le mot de passe rentré dans notre formulaire correspond bien à celui récupéré dans notre BDD
    # Bien évidemment tous nos mots de passe sont alors cryptés à l'aide de la méthode BCrypt
    if BDDmdp != None and bcrypt.check_password_hash(BDDmdp[0], mdp):
        session[request.headers.get("X-Forwarded-For")] = identifiant # On stocke alors notre identifiant dans notre dictionnaire session afin de le réutiliser plus tard
        return redirect('/index')# Une fois connecté on est alors redirigé vers la page index 
    else:
        return redirect('/')# Si les mots de passe ou les identifiants ne coïncident pas, la page de connexion est alors rafraîchie 


# Page servant à se déconnecté de la session courante
@app.route('/deconnexion')
def deconnexion():
    session.pop(request.headers.get("X-Forwarded-For"), None) # On ferme la session
    return redirect('/')# On est alors redirigé vers la page de connexion

# Page affichant la liste entière des étudiants présents dans notre BDD
@app.route('/index')
def index():
    if(request.headers.get("X-Forwarded-For") in session ):# On vérifie que l'utilisateur est bien connecté à la session afin de ne pas pouvoir accéder à la page sans être connecté d'avance
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
        conn.text_factory = str
        cur = conn.cursor()
        # On va alors créer une table dans notre BDD qui contiendra la liste de tous nos étudiants
        cur.execute("CREATE TABLE IF NOT EXISTS Etudiant (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, Nom VARCHAR(100) NOT NULL, Prenom VARCHAR(100) NOT NULL, Promo VARCHAR(100) NOT NULL, Presence VARCHAR(45) NOT NULL, Photo1 BLOB NOT NULL, Photo2 BLOB NOT NULL, Photo3 BLOB NOT NULL, Photo4 BLOB NOT NULL, Photo5 BLOB NOT NULL, Photo6 BLOB NOT NULL, Photo7 BLOB NOT NULL)")
        cur.execute("SELECT * FROM Etudiant") # On récupère alors la liste de tous nos étudiants dans le curseur
        posts = cur.fetchall()# On place alors les éléments du curseur dans une variable de type tuple
        cur.close()
        conn.close()
        # On affiche la page correspondante au lancement de la page, et on envoie les valeurs de noter posts à la page html
        return render_template('dashboard.html', posts = posts, identifiant = session[request.headers.get("X-Forwarded-For")])

    else:
        return redirect('/')  

# Page affichant le dormulaire servant à ajouter des étudiants à la BDD
@app.route('/ajouter')
def pageAjouter():
    if(request.headers.get("X-Forwarded-For") in session):
        return render_template('ajouter.html', identifiant = session[request.headers.get("X-Forwarded-For")])
    else:
        return redirect('/')

# Page de vérification de l'ajout d'un étudiant
@app.route('/valid', methods=['POST'])
def ajouterEtRetour():
    if(request.headers.get("X-Forwarded-For") in session):
        try :
            nom = request.form['nom']
            prenom = request.form['prenom']
            promo = request.form['promo']
            pic1 = request.files.getlist('photo1')
            print("JE SUIS LAAAAAAAAAAAAAAAAAAAAAAA")
            print(pic1)
            image=[]
            for picture in pic1:
                image.append(picture)
            print("JE SUIS LAAAAAAAAAAAAAAAAAAAAAAA22222222222")
            print(image[0])
            # pic2 = request.files['photo2']
            # pic3 = request.files['photo3']
            # pic4 = request.files['photo4']
            # pic5 = request.files['photo5']
            # pic6 = request.files['photo6']
            # pic7 = request.files['photo7']
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            # On stocke la commande SQL à effectuer pour ajouter notre étudiant à la BDD afin de ne pas avoir une commande trop longue par la suite
            sql = "INSERT INTO Etudiant (Nom, Prenom, Promo, Presence, Photo1, Photo2, Photo3, Photo4, Photo5, Photo6, Photo7) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # On convertit toutes nos photos en BlobFile afin de pouvoir les stocker convenablement en BDD
            blobFile1 = image[0].read()
            blobFile2 = image[1].read()
            blobFile3 = image[2].read()
            blobFile4 = image[3].read()
            blobFile5 = image[4].read()
            blobFile6 = image[5].read()
            blobFile7 = image[6].read()
            # On vérifie si il n'existe pas un étudiant avec la même combinaison Nom/Prenom dans la BDD et dans celui que l'on veut ajouter 
            cur.execute("SELECT * FROM etudiant WHERE Nom LIKE '" + nom + "%' AND Prenom LIKE '" + prenom + "%'")
            # Si jamais on trouve un étudiant avec la même combinaison de Nom/Prenom, on lui ajoute un numéro à la fin pour le différencier des autres et éviter d'avoir des doublons en BDD
            long = len(cur.fetchall())
            if long > 0:
                nom = nom + str(long) # On ajoute la valeur de notre long, convertit en string, à notre variable de base
                prenom = prenom + str(long)
            # On définit le set de valeurs à envoyer dans la BDD
            value = (nom, prenom, promo, '$', blobFile1, blobFile2, blobFile3, blobFile4, blobFile5, blobFile6, blobFile7)
            cur.execute(sql, value)
            conn.commit()
            # On  récupère le informations du dernier étudiant ajouté en BDD afin de vérifier qu'il a bien été ajouté dans la BDD et que l'utilisateur puisse vérifier les informations rentrées
            cur.execute( "SELECT Nom, Prenom, Promo FROM Etudiant WHERE id = (SELECT MAX(id) FROM Etudiant)")
            validation = cur.fetchone()
            cur.close()
            conn.close()

        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)

        return render_template('valid.html', validation = validation, identifiant = session[request.headers.get("X-Forwarded-For")])

    else:
        return redirect('/')

# Page nous permettant d'ajouter des utilisateurs
@app.route("/ajouterCo")
def ajouterCo():
    administrateur = "Administrateur"
    if(request.headers.get("X-Forwarded-For")  in session):
        if (administrateur == session[request.headers.get("X-Forwarded-For")]) :
            return render_template("ajouterCo.html", identifiant = session[request.headers.get("X-Forwarded-For")])

        else :
            return redirect ('/')

    else :
        return redirect('/')

# Page permettant d'ajouter l'utilisateur à la table connexion de notre BDD
@app.route('/validCo', methods=['POST'])
def ajouterIdentifiant():  
    if(request.headers.get("X-Forwarded-For")  in session):
        administrateur = "Administrateur"
        if (administrateur == str(session[request.headers.get("X-Forwarded-For")])) :
            try :
                identifiant = request.form['identifiant']
                password = request.form['password']
                validation = []
                validation.extend(identifiant)
                pw_hash = bcrypt.generate_password_hash(password)# On crypte notre mot de passe à l'aide de la méthode BCrypt
                conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
                conn.text_factory = str
                cur = conn.cursor()
                sql = "INSERT INTO connexion (Identifiant, Password) VALUES (%s,%s)"
                value = (identifiant, pw_hash)
                cur.execute(sql, value)
                conn.commit()
                cur.close()
                conn.close()

            except mysql.connector.Error as error:
                print("Erreur lors de l'insertion", error)
    
            return render_template("validation.html", validation = validation, identifiant = session[request.headers.get("X-Forwarded-For")])
        else :
            return redirect ('/')

    else :
        return redirect('/')


# Page affichant la liste des étudiants en affichant une seule année à la fois
@app.route('/annee', methods=['POST'])
def triAnnee():
    if(request.headers.get("X-Forwarded-For") in session ):
        try:
            annee = request.form['annee']
            annees = []
            annees.append(annee)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            # On effectue une verification pour les années 4 et 5 car il n'y a pas de 4 ou de 5 pour identifier l'année en BDD
            if annees[0] == '4':
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'M1')")

            elif annees[0] == '5':
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'M2')")

            else :
                cur.execute("SELECT * FROM Etudiant WHERE (Promo = 'CIR" + annee + "' OR Promo = 'CPG" + annee + "' OR Promo = 'CNB" + annee + "')")
            posts = cur.fetchall()
            return render_template('annee.html', posts = posts, annee = annees, identifiant = session[request.headers.get("X-Forwarded-For")])
        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)
    else:
        return redirect('/')
    
    
# Page affichant la liste des étudiants en affichant une seule promotion à la fois
@app.route('/promo', methods=['POST'])
def triPromo():
    try :
        if(request.headers.get("X-Forwarded-For") in session ):
            promo = request.form['promo']
            promos = []
            promos.append(promo)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute("SELECT * FROM Etudiant WHERE (Promo = '" + promo + "')")
            posts = cur.fetchall()
            return render_template('promo.html', posts = posts, promo = promos, identifiant = session[request.headers.get("X-Forwarded-For")])

        else:
            return redirect('/')
    
    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion", error)

# Page affichant un graphique montrant la porportion entre les élèves présents et absents
@app.route('/graphe')
def graphes():
    if(request.headers.get("X-Forwarded-For") in session ):
        conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute("SELECT * FROM Etudiant")
        posts = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM Etudiant WHERE Presence = '%'")# On récupère le nombre d'élèves présents en ce moment
        presences = cur.fetchone()[0] # On l'ajoute à notre tableau 
        cur.execute("SELECT COUNT(*) FROM Etudiant WHERE Presence = '$'")# On récupère le nombre d'élèves absents en ce moment
        absences = cur.fetchone()[0]
        cur.close()
        conn.close()
        try:
            pctPre = round(presences/(presences + absences) * 100, 2)# On calcule le pourcentage d'élèves présents en arrondissant au centième
            pctAbs = round(absences/(presences + absences) * 100, 2)# On calcule le pourcentage d'élèves absents en arrondissant au centième
            pct = []
            pct.append(pctPre)
            pct.append(pctAbs)
            return render_template('graphes.html', posts = posts, presences = presences, absences = absences, pct = pct, identifiant = session[request.headers.get("X-Forwarded-For")])
        except:
            print("erreur division par zero")
            return redirect('/index') 


    else:
        return redirect('/') 

# Page nous servant à supprimer un étudiant de la BDD
@app.route('/supprimer')
def pageSupprimer():
    if (request.headers.get("X-Forwarded-For") in session) :
        return render_template('supprimer.html', identifiant = session[request.headers.get("X-Forwarded-For")])
    else:
        return redirect('/')

# Page de validation, de vérification et qui effectue la suppression de l'étudiant
@app.route('/validSuppr', methods=['POST'])
def supprimer():
    if (request.headers.get("X-Forwarded-For") in session) :
        validations=[]
        try :
            nom = request.form['nom']
            prenom = request.form['prenom']
            promo = request.form['promo']
            validations.append(nom)
            validations.append(prenom)
            validations.append(promo)
            conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
            conn.text_factory = str
            cur = conn.cursor()
            cur.execute("SELECT id FROM etudiant WHERE Nom = '" + nom + "' AND Prenom = '" + prenom + "' AND Promo = '" + promo + "'")
            id = cur.fetchone()
            if(id!=None):
                idstr = str(id[0])
                cur.execute("DELETE FROM etudiant WHERE id = '" + idstr + "'")
                conn.commit()
                cur.close()
                conn.close()
            else:
                cur.close()
                conn.close()
                return render_template('IncorrectSuppr.html', identifiant = session[request.headers.get("X-Forwarded-For")])

        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)

        return render_template('validSuppr.html',validations=validations, identifiant = session[request.headers.get("X-Forwarded-For")])

    else:
        return redirect('/') 

# Page de paramètres nous permettant de modifier le mot de passe de la session courante
@app.route('/settings')
def settings():
    if(request.headers.get("X-Forwarded-For")  in session):
        return render_template('settings.html', identifiant = session[request.headers.get("X-Forwarded-For")])
    else:
        return redirect('/')

# Page de modification effective du mot de passe
@app.route('/newMDP', methods=['POST'])
def newMDP():
    if(request.headers.get("X-Forwarded-For")  in session):
        try:
            identifiant = request.form['identifiant']
            if(identifiant == session[request.headers.get("X-Forwarded-For")]):
                ancienMDP = request.form['ancienMDP']
                nouveauMDP = request.form['nouveauMDP']
                conn = mysql.connector.connect(host="eu-cdbr-west-01.cleardb.com", user="bc534e43745e55", password="3db62771", database="heroku_642c138889636e7")
                conn.text_factory = str
                cur = conn.cursor()
                cur.execute("SELECT Password FROM connexion WHERE Identifiant = '" + identifiant + "'")
                password = cur.fetchone()
                # On compare notre mot de passe en BDD avec notre ancien mot de passe du formulaire en utilisant la méthode donnée par BCrypt
                if(bcrypt.check_password_hash(password[0], ancienMDP)):
                    pw_hash = bcrypt.generate_password_hash(nouveauMDP)
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
                return redirect('/index')

            return redirect('/settings')

        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion", error)
    else:

        return redirect('/')