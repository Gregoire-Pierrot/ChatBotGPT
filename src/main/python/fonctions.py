from fpdf import FPDF
import qrcode
import requests
import base64
import qrcode
import os


##############################################################
                        # Fonctions #
##############################################################



####################################################
# Ecrire un message dans le pdf
####################################################

def write_message(message, pdf, color):
    if message.strip():
        pdf.set_text_color(color[0], color[1], color[2])
        pdf.multi_cell(0, 10, message)
        pdf.ln()


####################################################
# Faire le PDF en fonction des messages
####################################################

def make_pdf(historic):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVuSans", "", "DejaVuSans.ttf")
    pdf.set_font("DejaVuSans", size=12)

    i = 0
    print(len(historic))
    color1 = [255, 0, 0]
    color2 = [0, 0, 255]
    while i < len(historic):
        print(historic[i])
        print(historic[i+1])
        write_message(historic[i], pdf, color1)
        write_message(historic[i+1], pdf, color2)
        i += 2

    pdf.output("pdf/conversation.pdf")


######################################################
# Prendre le token github du fichier github_token.txt
######################################################

def get_token():
    # Prendre le token github
    with open("github_token.txt", "r") as fichier:
        contenu = fichier.read()

    if contenu is None:
        print("Le contenu du fichier github_token.txt est vide.")
        exit()

    print(contenu)
    return contenu


######################################################
# Supprimer le pdf et le qrcode si existant
######################################################

def prepare_github(url, headers, username, repository, qrcode_path):
    # Étape 1 : Supprimer le fichier PDF, s'il existe
    # Obtenir le SHA du fichier PDF
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha_pdf = response.json()["sha"]
        # Supprimer le fichier PDF avec le SHA
        delete_data = {
            "message": "Suppression de l'ancien PDF",
            "sha": sha_pdf,
            "content" : ""
        }
        response = requests.put(url, headers=headers, json=delete_data)
        if response.status_code == 204:
            print("Précédent PDF supprimé avec succès !")
        else:
            print("Erreur lors de la suppression du PDF :", response.json())
    else:
        print("Pas de PDF déjà existant.")

    # Étape 2 : Supprimer le fichier QR code, s'il existe
    # Obtenir le SHA du fichier QR code
    url_qrcode = f"https://api.github.com/repos/{username}/{repository}/contents/{qrcode_path}"
    response = requests.get(url_qrcode, headers=headers)
    if response.status_code == 200:
        sha_qrcode = response.json()["sha"]
        # Supprimer le fichier QR code avec le SHA
        delete_data = {
            "message": "Suppression de l'ancien QR code",
            "sha": sha_qrcode,
            "content" : ""
        }
        response = requests.put(url_qrcode, headers=headers, json=delete_data)
        if response.status_code == 204:
            print("Précédent QR code supprimé avec succès !")
        else:
            print("Erreur lors de la suppression du QR code :", response.json())
    else:
        print("Pas de QR code déjà existant.")


######################################################
# Créer le qrcode
######################################################

def create_qrcode(file_url):
    # Générer le QR code pour le lien
    qr = qrcode.make(file_url)
    qr.save("qrcode/qrcode.png")
    print("QR code généré et enregistré sous 'qrcode.png'")


######################################################
# Envoyer le pdf et le qrcode au github
######################################################

def sendPDF_to_github(url, headers, content, username, repository, branch, file_path):
    # Envoyer la requête GET pour obtenir le SHA du dernier commit
    response = requests.get(url, headers=headers)
    sha = None
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        print("Erreur lors de l'obtention du SHA du PDF:", response.json())
        exit()
    
    data = {
        "message": "Upload du fichier PDF",
        "content": content,
        "branch": branch,
        "sha": sha
    }

    # Envoyer la requête PUT pour téléverser le fichier PDF
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Fichier PDF uploadé avec succès !")
        # Générer le lien de téléchargement direct
        file_url = f"https://github.com/{username}/{repository}/raw/{branch}/{file_path}"
        print("Lien de téléchargement :", file_url)
        return file_url
    else:
        print("Erreur lors de l'upload du PDF:", response.json())
        return None
    

######################################################
# Envoyer le pdf et le qrcode au github
######################################################

def sendQRCODE_to_github(url_qrcode, headers, content, branch):
    # Envoyer la requête GET pour obtenir le SHA du dernier commit
    response = requests.get(url_qrcode, headers=headers)
    sha = None
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        print("Erreur lors de l'obtention du SHA du QRCode:", response.json())
        exit()
    
    data = {
        "message": "Upload du fichier QRCode",
        "content": content,
        "branch": branch,
        "sha": sha
    }

    # Envoyer la requête PUT pour téléverser le fichier PDF
    response = requests.put(url_qrcode, headers=headers, json=data)
    if response.status_code == 200:
        print("QRCode uploadé avec succès !")
    else:
        print("Erreur lors de l'upload du QRCode :", response.json())


######################################################
# Créer le QR code
######################################################

def make_qrcode():
    token = get_token()
    username = "YgueOne"
    repository = "ChatBotGPT"
    file_path = "src/main/python/pdf/conversation.pdf"
    file_name = "pdf/conversation.pdf"
    qrcode_path = "src/main/python/qrcode/qrcode.png"
    branch = "main"

    url = f"https://api.github.com/repos/{username}/{repository}/contents/{file_path}"
    with open(file_name, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    file_url = sendPDF_to_github(url, headers, content, username, repository, branch, file_path)
    if file_url is None:
        exit()

    url_qrcode = f"https://api.github.com/repos/{username}/{repository}/contents/{qrcode_path}"
    create_qrcode(file_url)

    sendQRCODE_to_github(url_qrcode, headers, content, branch)

    # Afficher le QR code
    os.system("qrcode/qrcode.png")

######################################################