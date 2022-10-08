# -*- coding: utf-8 -*-

# importando librerias necesarias 
from tkinter import Tk, Button, Label, filedialog
import base64
from tkinter import *
import grpc
from PIL import Image
from PIL import ImageTk
import numpy as np

import backend_pb2
import backend_pb2_grpc
#my package
import tkinter.messagebox

from tkinter import messagebox

#--------------------------------------

str_path = None
panelA = None
panelB = None


#Inicializando la ventana de herramientas 
root = Tk()



def select_image():
    # se usa una imagen de referencia para los paneles
    global panelA, backend_client, img_content, img_w, img_h, str_path
    # abrir un cuadro de diálogo de selección de archivos y permitir que el usuario seleccione una entrada
    # imagen
    path = filedialog.askopenfilename()
    str_path = path
    # asegurando que la ruta tomó el archivo
    if len(path) > 0:
        
        path_message = backend_pb2.img_path(path=path)
        response = backend_client.load_image(path_message)

        img_content = response.img_content
        img_w = response.width
        img_h = response.height

        b64decoded = base64.b64decode(img_content)
        image = np.frombuffer(b64decoded, dtype=np.uint8).reshape(img_h, img_w, -1)

        # convirtiendo las imagenes en  formato PIL 
        image = Image.fromarray(image)
        
        
        
        #Imagen en formato ImageTk
        image = ImageTk.PhotoImage(image)

        #si el panel es None, inicialicelos 
        if panelA is None:
            #el primer panel almacenará nuestra imagen original
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            button1['state'] = 'normal'
        else:
            panelA.configure(image=image)
            panelA.image = image

def prediction():
    global panelB, backend_client, str_path


    if len(str_path) > 0:
        
        
        path_msg = backend_pb2.image_data(path2=str_path)
        response = backend_client.predict_data(path_msg)

        v_percent = response.proba
        v_result = response.label
        result_prediction = "De acueardo al Resultado de la evaluación de la imagen\n el paciente presenta un tipo de neumonia {}, \n con una probabilidad de {:.2f}%".format(v_result, v_percent)

        messagebox.showinfo(title=None, message=result_prediction)


    else:
        messagebox.showerror('El path viene vacio')


root.title("Detector de Neumonía")
root.resizable(0, 0)



#Definicion del backend del cliente


maxMsgLength = 1024 * 1024 * 1024
options = [('grpc.max_message_length', maxMsgLength), ('grpc.max_send_message_length', maxMsgLength), ('grpc.max_receive_message_length', maxMsgLength)]
channel = grpc.insecure_channel("backend:50051", options = options)
backend_client = backend_pb2_grpc.BackendStub(channel=channel)
## Boton predict
button1 = Button(root, text="Predecir",  command=prediction) 
button1.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()
