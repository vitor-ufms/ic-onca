import os
from exif import Image as Im
from PIL import Image
from datetime import date
import pandas as pd
from tkinter import *


#############################################
try:
    os.mkdir("Dados")
except:
    print("A pasta Dados já existe")
    
try:
    os.mkdir("Imagem")
except:
    print("A pasta Imagem já existe")



d = { 'Coordenada(DMS)':[],
    'Coordenada_lat(DD)':[],
    'Coordenada_long(DD)':[],
    'altitude':[],
    'Assunto':[],
    "Texto":[],
    'ID':[],
    'fileName': [],
    "Data_foto": [],
    'Data_email': [],
    'From_Email': []
     }

############################################################

# graus decimais
def dec_coord(coords, ref): 
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600 
    if ref == 'S' or ref == 'W': 
        decimal_degrees = -decimal_degrees 
    return decimal_degrees

#############################################################
# DMS, DD_lat, DD_log, altitude, data_foto
def prop_img(fileName):

    end_img =  'Imagem' + os.sep + fileName 

    with open(end_img, 'rb') as arq_img: ## wb escrita
        img = Im(arq_img)
        if(img.has_exif):
            try:
                DMS = []
                DMS.append(img.gps_latitude)
                DMS.append(img.gps_latitude_ref)
                DMS.append(img.gps_longitude)
                DMS.append(img.gps_longitude_ref)

                DD_lat = dec_coord(img.gps_latitude,img.gps_latitude_ref)
                DD_lon = dec_coord(img.gps_longitude, img.gps_longitude_ref)
                altitude = img.gps_altitude
                data_foto = img.datetime_original
                
                return str(DMS), DD_lat, DD_lon, altitude, data_foto
            except:
                print('erro no exif')
                return 'NA', 'NA','NA','NA','NA'
        else:
            print('Não tem exif')
            return 'NA','NA','NA','NA','NA'


######################################################3

def email(EMAIL,PASSWORD):
    import email
    import imaplib

    #EMAIL = 'jaguarfb2015@gmail.com'
    #PASSWORD ='toorpljtqpzkgqif'

    SERVER = 'imap.gmail.com'

    # abriremos uma conexão com SSL com o servidor de emails
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)

    # selecionamos a caixa de entrada neste caso
    mail.select('inbox')

    status, data = mail.search(None, 'ALL')
    # Busca em email que não foram abertos
    #status, data = mail.search(None, ('UNSEEN'))

    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        # a função fetch baixa o email passando id e o formato
        status, data = mail.fetch(i, '(RFC822)')
    
        message1 = email.message_from_string(data[0][1].decode('utf-8'))
        list_fileName = []

        Data_E = message1['Date']
        From = message1['From']
        for a in message1.walk():
            #print('AA:\n',a)
            #a.append('===========fim do a ----------------')
            if a.get_content_type() == 'image/jpeg':
                fileName = a.get_filename()
                foto = a.get_payload(decode=True)
                #print('fileName2: ',fileName)
                with open(f'Imagem{os.sep}{fileName}','wb')as arquivo:
                    arquivo.write(foto)
                list_fileName.append(fileName)

            if a.get_content_type() == 'application/octet-stream':
                fileName = a.get_filename()
                foto = a.get_payload(decode=True)
                #print('fileName1: ',fileName)
                with open(f'Imagem{os.sep}{fileName}','wb')as arquivo:
                    arquivo.write(foto)
                list_fileName.append(fileName)

            if a.get_content_type() == 'text/plain':
                msg = a.get_payload()
            # print('mensagem: ',msg)

            if a.get('Subject') is not None:
                ass = a.get('Subject') 
                #print('assunto: ',ass)
        
        #Escrevendo na planilha 
        if len(list_fileName) > 0:  # tem foto?
            print("################### Entrou ####################3")
            for fileName in list_fileName: # percorre cada foto 
                DMS, DD_lat, DD_log, altitude, data_foto = prop_img(fileName) # coord igual a -1 se não tem exif

                d['Coordenada(DMS)'].append(DMS)
                d['Coordenada_lat(DD)'].append(DD_lat)
                d['Coordenada_long(DD)'].append(DD_log)
                d['altitude'].append(altitude)
                d['Data_foto'].append(data_foto)
                

                d['Assunto'].append(ass)
                d['fileName'].append(fileName)
                d['ID'].append(i)
                d['Texto'].append(msg)
                d['From_Email'].append(From)
                d['Data_email'].append(Data_E)

        print('FRom: ',From)
        print("DATA Email: ", Data_E)
        print('id = ',i)
        print('------------------------outro email-----------------------------------------------')

        texto = Label(janela, text="From: "+ From)
        texto.grid(column=0, row=4, padx=100, pady=100)

        texto = Label(janela, text="Data Email: " + Data_E)
        texto.grid(column=0, row=5, padx=10, pady=10)

        texto = Label(janela, text="id: "+ str(i))
        texto.grid(column=0, row=6, padx=10, pady=10)
        janela.update()


    finalizando(EMAIL)
###################################################

def finalizando(EMAIL):
    print('Gravando os dados em excel')

    data_atual = date.today()

    nome_planilha = EMAIL + "." + str(data_atual)

    dados = pd.DataFrame(data=d)
    dados.to_excel(f'Dados{os.sep}{nome_planilha}.xlsx', index=False)

    print('imprimindo os dados da planilha')
    matrix = pd.read_excel(f'Dados{os.sep}{nome_planilha}.xlsx')
    print(matrix)

    print("Fim da execucao")



########################################## Janela #################33
def iniciar():
   EMAIL = entry_email.get()
   PASSWORD = entry_key.get()

   entry_key.delete(0, END) # limpa a senha
   entry_key.insert(0, "*************")

   texto = Label(janela, text='Processando...',background= "blue")
   texto.grid(column=1, row=2, padx=10, pady=10)
   janela.update()

   email(EMAIL, PASSWORD)

   texto = Label(janela, text='Fim do processamento, tudo Ok!',background= "red")
   texto.grid(column=1, row=2, padx=10, pady=10)
   janela.update()


janela = Tk()

janela.iconbitmap('aa.ico') # verificar se esta na mesma pasta
janela.title('Jaguar')
#janela.iconbitmap('onca.jpg')
janela.geometry('1000x600')

botao = Button(janela, text='Iniciar programa', command= iniciar)
botao.grid(column=0, row=1, padx=10, pady=10)

texto_resposta = Label(janela, text='texto de resposta')
texto_resposta.grid(column=0, row=2, padx=10, pady=10)

entry_email = Entry(fg="black", bg="white", width=50)
entry_email.grid(column=0, row=3, padx=10, pady=10)
entry_email.insert(0, "jaguarfb2015@gmail.com")

entry_key = Entry(fg="black", bg="white", width=50)
entry_key.grid(column=1, row=3, padx=10, pady=10)
entry_key.insert(0, "toorpljtqpzkgqif")

janela.mainloop()

input("Pressione <enter> para encerrar!")