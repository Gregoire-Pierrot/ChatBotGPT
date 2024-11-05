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

    return contenu


######################################################
# Supprimer le pdf et le qrcode déjà existant
######################################################

def prepare_github(url, headers, username, repository, qrcode_path):
    # Supprimer le fichier existant si il existe
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Précédent PDF supprimé avec succès !")
        url_qrcode = f"https://api.github.com/repos/{username}/{repository}/contents/{qrcode_path}"
        response = requests.delete(url_qrcode, headers=headers)
        if response.status_code == 204:
            print("Précédent QR code supprimé avec succès !")
        else:
            print("Pas de qrcode déjà existant.")
    else:
        print("Pas de PDF déjà existant.")


######################################################
# Envoyer le pdf et le qrcode au github
######################################################

def send_to_github(url, headers, data, username, repository, branch, file_name):
    # Envoyer la requête PUT pour téléverser le fichier
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Fichier uploadé avec succès !")
        # Générer le lien de téléchargement direct
        file_url = f"https://github.com/{username}/{repository}/raw/{branch}/{file_name}"
        print("Lien de téléchargement :", file_url)
        
        # Générer le QR code pour le lien
        qr = qrcode.make(file_url)
        qr.save("qrcode/qrcode.png")
        print("QR code généré et enregistré sous 'qrcode.png'")
    else:
        print("Erreur lors de l'upload :", response.json())


######################################################
# Créer le QR code
######################################################

def make_qrcode():
    token = get_token()
    username = "YgueOne"
    repository = "ChatBotGPT"
    file_path = "pdf/conversation.pdf"
    file_name = "src/main/python/pdf/conversation.pdf"
    qrcode_path = "src/main/python/qrcode/qrcode.png"
    branch = "main"

    url = f"https://api.github.com/repos/{username}/{repository}/contents/{file_name}"
    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": "Upload du fichier PDF",
        "content": content,
        "branch": branch
    }

    prepare_github(url, headers, username, repository, qrcode_path)
    send_to_github(url, headers, data, username, repository, branch, file_name)

    # Afficher le QR code
    os.system("qrcode/qrcode.png")

######################################################