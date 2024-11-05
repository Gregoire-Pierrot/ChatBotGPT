from config import sendMessage
from config import config
from fonctions import make_pdf, make_qrcode


####################################################
                    # Execution #
####################################################
historic = []
while True:
    message = input("Enter your message : ")
    if message == "exit":
        break
    historic.append(message)
    historic.append(sendMessage(message, "French", config))

make_pdf(historic)
make_qrcode()

####################################################