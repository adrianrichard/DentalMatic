from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import util.config as utl
from bd.conexion import Conexion
from PIL import Image, ImageGrab, ImageDraw, ImageTk
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import platform
import subprocess
import os
import re
pacientes=[]
buttons = []

class Odontograma:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dni_paciente = StringVar()
        self.ID_odonto = StringVar()
        self.ID_odonto= 0
        self.fuenten= utl.definir_fuente()
        self.fuenteb= utl.definir_fuente_bold()
        self.db = Conexion()
        self.miConexion = self.db.conectar()

    def ventana_odonto(self):
        self.ventana_odontograma= tk.Toplevel()
        self.ventana_odontograma.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_odontograma.focus_set() # Mantiene el foco cuando se abre la ventana.

        self.ventana_odontograma.geometry('750x500')
        self.ventana_odontograma.grid_columnconfigure(0, weight= 1)
        self.ventana_odontograma.configure(bg= "gray")
        utl.centrar_ventana(self.ventana_odontograma, 920, 500)
        self.fecha_actual = datetime.now().date()
        self.fecha_actual = self.fecha_actual.strftime("%d-%m-%Y")
        Label(self.ventana_odontograma, text= 'Odontograma', font= 'Arial 20 bold', bg= "gray", fg= 'white').grid(column= 0, row= 0)

        apellido= self.paciente[0]
        nombre= self.paciente[1]
        dni= self.paciente[2]
        fechanac= self.convertir_fecha(self.paciente[3])
        obra_social= self.paciente[4]
        nrosocio= self.paciente[5]

        self.frame_datos_paciente=Frame(self.ventana_odontograma, border= 1, borderwidth= 2, bg= "gray90")
        self.frame_datos_paciente.grid(column= 0, row= 1, sticky= "nsew")
        Label(self.frame_datos_paciente, text= 'Nombre Completo:', font= self.fuenteb, bg= "gray90").grid(column= 0, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= apellido+', '+nombre, font= self.fuenten, bg= "gray90").grid(column= 1, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'D.N.I.:', font= self.fuenteb, bg= "gray90").grid(column= 2, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= dni, font= self.fuenten, bg= "gray90").grid(column= 3, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Fecha de nacimiento:', font= self.fuenteb, bg= "gray90").grid(column= 4, row= 0, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= fechanac, font= self.fuenten, bg= "gray90").grid(column= 5, row= 0, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Obra Social: ',  font= self.fuenteb, bg= "gray90").grid(column= 0, row= 1, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= obra_social, font= self.fuenten, bg= "gray90").grid(column= 1, row= 1, sticky= 'w', padx= (0, 10))
        Label(self.frame_datos_paciente, text= 'Nº socio: ',  font= self.fuenteb, bg= "gray90").grid(column= 2, row= 1, sticky= 'e', padx= (5, 0))
        Label(self.frame_datos_paciente, text= nrosocio, font= self.fuenten, bg= "gray90").grid(column= 3, row= 1, sticky= 'w', padx= (0, 10))
        self.ancho = 700

        self.cargar_odontologos()
        self.selector_odontologo= ttk.Combobox(self.frame_datos_paciente, state= "readonly", values= self.valores_combobox, width= 40, justify= CENTER, background= "white")
        self.selector_odontologo.grid(column= 5, row= 1, sticky= 'w', padx= (5, 10))
        self.selector_odontologo.set("Odontólogo")
        if self.valores_combobox == []:
            self.selector_odontologo.set("No hay odontologos")
        self.aviso_odontologo = Label(self.frame_datos_paciente, text= '', font= self.fuenteb, bg= "gray90")
        self.aviso_odontologo.grid(column= 4, row= 1, sticky= 'e', padx= (5, 0))

        self.frame_dientes = Frame(self.ventana_odontograma)
        self.frame_dientes.grid(column= 0, row= 3, pady= (10, 10))
        self.iniciar_odontograma()
        self.cargar_odontograma()
        self.cargar_dientes(self.ID_odonto)
        self.canvas = tk.Canvas(self.frame_dientes, width= self.ancho-20, height= 300)
        self.canvas.grid(row= 0, column= 0, columnspan=3, padx= 10)
        self.crear_dientes()

        self.boton_guardar_odonto=Button(self.frame_dientes, text= 'Guardar', command= self.guardar_odontograma, font= self.fuenteb, bg= '#1F704B', fg= 'white', width= 8)
        self.boton_guardar_odonto.grid(row= 1, column= 0, padx= 10, pady= 10)
        self.boton_PDF=Button(self.frame_dientes, text= 'Crear PDF', command= self.crear_pdf, font= self.fuenteb, fg= 'white', bg= "blue", width= 8)
        self.boton_PDF.grid(row= 1, column= 1, padx= 0)
        self.boton_salir_odonto=Button(self.frame_dientes, text= 'Salir', command= self.salir, font= self.fuenteb, fg= 'white', bg= "orange", width= 8)
        self.boton_salir_odonto.grid(row= 1, column= 2, padx= (0, 10))
        self.ventana_odontograma.mainloop()

    def salir(self):
        self.ventana_odontograma.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon= 'warning', parent= self.ventana_odontograma)
        if answer:
            self.ID_odonto= self.ID_odonto+1
            try:
                self.miCursor.execute("DELETE FROM Dientes WHERE id_odonto=?", (self.ID_odonto,))
                self.miConexion.commit()
            except:
                self.ventana_odontograma.grab_set()
                return
            self.ventana_odontograma.destroy()
        else:
            self.ventana_odontograma.grab_set()

    def cargar_odontologos(self):
        self.cur= self.miConexion.cursor()
        self.lista_odontologos = []
        self.odontologos = []
        self.valores_combobox = []
        try:
            self.cur.execute("SELECT Matricula, Apellido_odontologo, Nombre_odontologo FROM odontologos ORDER BY Matricula")
            self.lista_odontologos = self.cur.fetchall()
            for matricula, nombre, apellido in self.lista_odontologos:
                texto = f"Mat. {matricula} - {apellido}, {nombre}"
                self.valores_combobox.append(texto)
            # Cargar el combobox
            self.valores_combobox
        except:
            self.ventana_odontograma.grab_release()
            messagebox.showinfo("Odontograma", "No hay odontologos cargados", parent= self.ventana_odontograma)
            self.ventana_odontograma.grab_set()

    def cargar_paciente(self, dni):
        self.dni_paciente = dni
        try:
            self.miCursor=self.miConexion.cursor()
            self.miCursor.execute("SELECT apellido, nombre, ID, fechanacimiento, obrasocial, nrosocio FROM Pacientes WHERE ID=?", (dni,))
            self.paciente = self.miCursor.fetchone()
            self.miConexion.commit()
        except:
            self.ventana_odontograma.grab_release()
            messagebox.showinfo("Odontograma", "No se cargo el paciente", parent= self.ventana_odontograma)
            self.ventana_odontograma.grab_set()

    def convertir_fecha(self, fecha):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_date = fecha_obj.date()
        return fecha_date.strftime("%d-%m-%Y")
    
    def iniciar_odontograma(self):
        self.miCursor=self.miConexion.cursor()
        self.crear_odontograma= False
        try:
            self.miCursor.execute("SELECT id_odontograma from Odontogramas WHERE dni_paciente=? ORDER BY id_odontograma DESC", (self.dni_paciente,))
            self.miConexion.commit()
            self.ID_odonto_actual= self.miCursor.fetchone()
            if not self.ID_odonto_actual:
                self.crear_odontograma= True
                self.ventana_odontograma.grab_release()
                messagebox.showinfo("Odontograma", "Crear odontograma", parent= self.ventana_odontograma)
                self.ventana_odontograma.grab_set()
        except:
            self.ventana_odontograma.grab_release()
            messagebox.showinfo("Odontograma", "Problema con BD", parent= self.ventana_odontograma)
            self.ventana_odontograma.grab_set()

    def cargar_odontograma(self):
        self.miCursor= self.miConexion.cursor()
        if self.crear_odontograma:
            try:
                self.miCursor.execute("SELECT id_odontograma from Odontogramas ORDER BY id_odontograma DESC")
                self.miConexion.commit()
                self.ID_odonto_actual= self.miCursor.fetchone()
                self.ID_odonto = self.ID_odonto_actual[0]
            except:
                return
        else:
            try:
                self.miCursor.execute("SELECT id_odontograma from Odontogramas WHERE dni_paciente=? ORDER BY id_odontograma DESC", (self.dni_paciente,))
                self.miConexion.commit()
                self.ID_odonto_actual= self.miCursor.fetchone()
                self.ID_odonto = self.ID_odonto_actual[0]
            except:
                self.ventana_odontograma.grab_release()
                messagebox.showinfo("Odontograma", "Crear odontograma", parent= self.ventana_odontograma)
                self.ventana_odontograma.grab_set()
                self.miCursor.execute("SELECT id_odontograma from Odontogramas ORDER BY id_odontograma DESC LIMIT 1")
                self.miConexion.commit()
                self.ID_odonto_actual= self.miCursor.fetchone()
                self.ID_odonto = self.ID_odonto_actual[0]

    def obtener_matricula(self, apellido):
        odontologo = self.selector_odontologo.get()
        match = re.search(r'Mat\.?\s*(\d+)', odontologo)
        try:
            odontologo = self.selector_odontologo.get()
            match = re.search(r'Mat\.?\s*(\d+)', odontologo)
            if match:
                return int(match.group(1))
            return None
        except (AttributeError, ValueError):
            return None

    def guardar_odontograma(self):
        self.ventana_odontograma.grab_release()
        answer = messagebox.askokcancel('Odontograma', '¿Desea guardar?', icon= 'warning', parent= self.ventana_odontograma)
        if answer:
            matricula=0
            if self.selector_odontologo.get() != 'Odontólogo':
                matricula = self.obtener_matricula(self.selector_odontologo.get().upper())
                f = datetime.today()
                fecha = f.strftime("%Y")+"-"+f.strftime("%m")+"-"+f.strftime("%d")
                datos= self.dni_paciente, fecha, matricula 
                try:
                    self.miCursor = self.miConexion.cursor()
                    sql = "INSERT INTO Odontogramas VALUES (NULL,?,?,?)"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    messagebox.showinfo("GUARDAR", "Odontograma guardado exitosamente", parent= self.ventana_odontograma)
                    self.ventana_odontograma.grab_set()
                    self.ventana_odontograma.destroy()
                except:
                    messagebox.showinfo("Odontograma", "No se pudo guardar el odontograma", parent= self.ventana_odontograma)
                    self.ventana_odontograma.grab_set()
            else:
                self.aviso_odontologo.config(text= "Elija un odontólogo", fg= 'red')
                messagebox.showinfo("Odontograma", "Elija un odontólogo", parent= self.ventana_odontograma)
                self.ventana_odontograma.grab_set()
        else:
            self.ventana_odontograma.grab_set()

    def crear_pdf(self):
        try:
            # Obtener la ruta del directorio donde está el script actual
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            directorio_padre = os.path.dirname(directorio_actual)
            
            # Carpeta odontogramas un nivel arriba del script
            carpeta_odontogramas = os.path.join(directorio_padre, "odontogramas")
            
            if not os.path.exists(carpeta_odontogramas):
                os.makedirs(carpeta_odontogramas)
            
            # Captura la ventana y guarda el área del Canvas
            x0 = self.frame_dientes.winfo_rootx() + self.canvas.winfo_x()
            y0 = self.frame_dientes.winfo_rooty() + self.canvas.winfo_y()
            x1 = x0 + self.canvas.winfo_width()
            y1 = y0 + self.canvas.winfo_height()
            imagen_canvas = ImageGrab.grab((x0, y0, x1, y1))

            temp_image_path = os.path.join(carpeta_odontogramas, "canvas_image.png")
            imagen_canvas.save(temp_image_path)

            apellido = self.paciente[0]
            nombre = self.paciente[1]
            dni = self.paciente[2]
            obra_social = self.paciente[4]
            nrosocio = self.paciente[5]

            nombre_archivo = f"{nombre}_{apellido}_{self.fecha_actual}.pdf"
            pdf_path = os.path.join(carpeta_odontogramas, nombre_archivo)

            pdf = pdf_canvas.Canvas(pdf_path, pagesize=A4)
            ancho_pagina, alto_pagina = A4

            carpeta_imagenes = os.path.join(directorio_padre, "imagenes")
            logo_path = os.path.join(carpeta_imagenes, "LOGO11.png")
            alto_imagen = 500

            if os.path.exists(logo_path):
                with Image.open(logo_path) as img:
                    logo_width, logo_height = img.size
                    escala_logo = min(alto_imagen / logo_width, alto_imagen / logo_height)
                    logo_width = int(logo_width * escala_logo)
                    logo_height = int(logo_height * escala_logo)
                    logo_x = (ancho_pagina - logo_width) / 2
                    logo_y = alto_pagina - 120

                pdf.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height)
            else:
                messagebox.showwarning("Odontograma", "Advertencia: No se encontró el logo")

            pdf.setFont("Helvetica", 15)
            pdf.setStrokeColor("black")
            pdf.setLineWidth(1)
            
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(ancho_pagina/2, alto_pagina - 150, "FICHA ODONTOLÓGICA")
        
            pdf.line(50, alto_pagina - 130, ancho_pagina - 50, alto_pagina - 130)
            
            datos_paciente = [
                ["APELLIDO/S Y NOMBRE/S", apellido + ", " + nombre],
                ["D.N.I.", dni],
                ["OBRA SOCIAL", obra_social],
                ["N° SOCIO", nrosocio],
                ["FECHA INFORME", self.fecha_actual]
            ]

            tabla_paciente = Table(datos_paciente, colWidths=[160, 335])
            tabla_paciente.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ]))
            tabla_paciente.wrapOn(pdf, ancho_pagina, alto_pagina)
            tabla_paciente.drawOn(pdf, 50, alto_pagina - 250)
            
            pdf.line(50, alto_pagina - 270, ancho_pagina - 50, alto_pagina - 270)
            
            temp_image_full_path = os.path.join(carpeta_odontogramas, "canvas_image.png")
            if os.path.exists(temp_image_full_path):
                with Image.open(temp_image_full_path) as img:
                    img_width, img_height = img.size
                    max_width = ancho_pagina - 100
                    max_height = alto_pagina - 200
                    escala_canvas = min(max_width / img_width, max_height / img_height)
                    img_width = int(img_width * escala_canvas)
                    img_height = int(img_height * escala_canvas)
                    captura_x = (ancho_pagina - img_width) / 2
                    captura_y = alto_pagina - 500
                pdf.drawImage(temp_image_full_path, captura_x, captura_y, width=img_width, height=img_height)
            
            pdf.line(50, 50, ancho_pagina - 50, 50)
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawCentredString(ancho_pagina/2, 30, f"MyM Odontología | {self.fecha_actual}")
            
            try:
                pdf.save()
                if os.path.exists(temp_image_full_path):
                    os.remove(temp_image_full_path)
                    
                self.ventana_odontograma.grab_release()
                messagebox.showinfo("Odontograma", f"Informe creado exitosamente", parent=self.ventana_odontograma)
                self.ventana_odontograma.grab_set()
                self.abrir_carpeta_contenedora(pdf_path)
            except Exception as e:
                if os.path.exists(temp_image_full_path):
                    os.remove(temp_image_full_path)
                    
                self.ventana_odontograma.grab_release()
                messagebox.showwarning("Odontograma", f"No se pudo crear el informe: {e}", parent=self.ventana_odontograma)
                self.ventana_odontograma.grab_set()
                
        except Exception as e:
            self.ventana_odontograma.grab_release()
            messagebox.showwarning("Odontograma", f"Error al crear el PDF: {e}", parent=self.ventana_odontograma)
            self.ventana_odontograma.grab_set()
        
    def abrir_carpeta_contenedora(self, filepath):
        try:
            sistema = platform.system()
            path_absoluto = os.path.abspath(filepath)
            
            if sistema == "Windows":
                # La mejor manera en Windows
                subprocess.run(f'explorer /select,"{path_absoluto}"', shell=True)
            elif sistema == "Darwin":  # macOS
                # Comando para macOS
                subprocess.run(['open', '-R', path_absoluto])
            else:  # Linux
                # Intentamos con los gestores de archivos más comunes
                try:
                    subprocess.run(['nautilus', '--select', path_absoluto])
                except FileNotFoundError:
                    try:
                        subprocess.run(['dolphin', '--select', path_absoluto])
                    except FileNotFoundError:
                        # Fallback: abrir solo la carpeta
                        subprocess.run(['xdg-open', os.path.dirname(path_absoluto)])
            
        except Exception as e:
            self.ventana_odontograma.grab_release()
            messagebox.showwarning("Odontograma", f"No se pudo abrir la carpeta: {e}", parent= self.ventana_odontograma)
            self.ventana_odontograma.grab_set()

    def crear_imagen_x(self, color):
        img = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.line((3, 3, 18, 18), fill= color, width= 3)
        draw.line((18, 3, 3, 18), fill= color, width= 3)
        return ImageTk.PhotoImage(img)
    
    def crear_imagen_circulo(self, color):
        radius= 10
        outline_width= 3
        size = radius * 2 + outline_width
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # Fondo transparente
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            (outline_width, outline_width, size-outline_width, size-outline_width),
            outline=color,
            width=outline_width
        )
        return ImageTk.PhotoImage(img)

    def editar_diente(self, numero):
        self.numero_actual = numero
        self.ventana_secundaria = tk.Toplevel()
        self.ventana_secundaria.title("Editar diente")
        #self.ventana_secundaria.geometry('300x350')
        self.ancho_ventana = 350
        self.alto_ventana = 400
        utl.centrar_ventana(self.ventana_secundaria, self.ancho_ventana, self.alto_ventana)
        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
        Label(self.ventana_secundaria, text= "EDITAR DIENTE", font= ("Arial", 15, 'bold'), fg= 'white', bg= "gray", width= 60).pack(pady= 10)
        Label(self.ventana_secundaria, text= "DIENTE "+str(numero), font= ("Arial", 12, 'bold'), fg= 'white', bg= "gray", width= 60).pack()
        diente_frame = Frame(self.ventana_secundaria)
        diente_frame.pack(pady= (10, 10))
        corona_extraccion_frame = Frame(self.ventana_secundaria, relief= "solid", borderwidth= 2)
        corona_extraccion_frame.pack(padx= (30, 30), pady= 5, fill= "x", expand= False)
        colores = ["blue", "green", "red"]
        for i, color in enumerate(colores):
            img = self.crear_imagen_x(color)
            btn = tk.Button(
                corona_extraccion_frame, 
                image= img, 
                compound= tk.TOP,
                command= lambda c= color: self.extraccion(c),
                bg="gray90"
            )
            btn.image = img
            btn.grid(row= 0, column= i+1, pady= 5, padx= 15)
        
        for i, color in enumerate(colores):
            img = self.crear_imagen_circulo(color)
            btn = tk.Button(
                corona_extraccion_frame, 
                image= img, 
                compound= tk.TOP,
                command= lambda c= color: self.corona(c),
                bg="gray90"
            )
            btn.image = img
            btn.grid(row= 1, column= i+1, pady= 5, padx= 15)
        Label(corona_extraccion_frame, text= "Extracción", font= ("Arial", 12)).grid(row= 0, column= 0, pady= 5, padx= (10, 20))
        Label(corona_extraccion_frame, text= "Corona", font= ("Arial", 12)).grid(row= 1, column= 0, pady= 5, padx= (10, 20))
        botones_frame = Frame(self.ventana_secundaria)
        botones_frame.pack()
        Button(botones_frame, text= 'Guardar', command= self.guardar_diente, font= self.fuenteb, bg= '#1F704B', fg= 'white', width= 8).grid(row= 2, column= 0, padx= 5)
        Button(botones_frame, text= 'Recargar', command= lambda n=numero: self.restablecer_diente(n), font= self.fuenteb, bg= "blue", fg= 'white', width= 8).grid(row= 2, column= 1, padx= 5)
        Button(botones_frame, text= 'Cancelar', command= self.cancelar, font= self.fuenteb, bg= "red", fg= 'white', width= 8).grid(row= 2, column= 2, padx= 5)
        self.canvas2 = tk.Canvas(diente_frame, width= 400, height= 150)
        self.canvas2.pack()
        self.cargar_diente(numero)

    def cargar_diente(self, numero):
        if self.dientes == []:
            self.diente_actual=[0, numero, self.ID_odonto, 'white','white','white','white','white','white','white']
        for diente in self.dientes:
            if diente[1] == numero:
                self.diente_actual= list(diente)
                break
            else:
                self.diente_actual= [0, numero, self.ID_odonto, 'white','white','white','white','white','white','white']

        width = 100
        height = 100
        x1 = (self.ancho_ventana - width) / 2
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        #LETRAS
        if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
            or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55:
            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue'  or self.diente_actual[9] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.diente_actual[9])
            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 2)
                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 2)
            else:
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[3], outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[5], outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[6], outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
        elif numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
            or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65:
            self.canvas2.create_text(x1+ width/2, 15, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'P', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue' or self.diente_actual[9] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.diente_actual[9])
            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 2)
                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 2)
            else:
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[5], outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[3], outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[6], outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')
          
            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
        elif numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
            or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue' or self.diente_actual[9] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.diente_actual[9])
            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 2)
                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 2)
            else:
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[5], outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[4], outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[3], outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[4], outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')

            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))
        elif numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
            or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85:
            self.canvas2.create_text(x1+ width/2, 15, text= 'L', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1-10, 25+ width/2, text= 'D', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width/2, 35+ height, text= 'V', fill= "black", font= ('Helvetica 10 bold'))
            self.canvas2.create_text(x1+ width+10, 25+ width/2, text= 'M', fill= "black", font= ('Helvetica 10 bold'))
            if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue'or self.diente_actual[9] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.diente_actual[9])
            elif self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
                self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 2)
                self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 2)
            else:
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.diente_actual[3], outline = "black", tags= 'C1')
                self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.diente_actual[6], outline = "black", tags= 'C2')
                self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[5], outline = "black", tags= 'C3')
                self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.diente_actual[4], outline = "black", tags= 'C4')
                self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.diente_actual[7], tags= 'CO')

            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))

        else:
            self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
            self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
            self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
            self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
            self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')

            self.canvas2.tag_bind('C1', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C1'))
            self.canvas2.tag_bind('C2', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C2'))
            self.canvas2.tag_bind('C3', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C3'))
            self.canvas2.tag_bind('C4', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'C4'))
            self.canvas2.tag_bind('CO', '<Button-1>', lambda event, num= numero: self.cambiar_color(event, num, 'CO'))

    def corona(self, color):

        if color == "red":
            self.diente_actual[9] = "red"
        elif color == "blue":
            self.diente_actual[9] = "blue"
        elif color == "green":
            self.diente_actual[9] = "green"

        width = 100
        height = 100
        x1 = (self.ancho_ventana - width) / 2
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
        self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
        self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
        self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
        if self.diente_actual[9] == 'red' or self.diente_actual[9] == 'blue'  or self.diente_actual[9] == 'green':
            self.canvas2.create_oval(x1+5, y1+5, x2-5, y2-5, width= 5, outline= self.diente_actual[9])
        for i in range (3, 10):
            if i != 9:
                self.diente_actual[i] = 'white'

    def determinar_color(self, color):
        if color == "white":
            bg='blue'
        elif color == "blue":
            bg='green'
        elif color == "green":
            bg='red'
        elif color == "red":
            bg='white'
        return bg
    
    def extraccion(self, color):
        if color == "red":
            self.diente_actual[8] = "red"
        elif color == "blue":
            self.diente_actual[8] = "blue"
        elif color == "green":
            self.diente_actual[8] = "green"

        width = 100
        height = 100
        x1 = (self.ancho_ventana - width) / 2
        y1 = 25
        x2 = x1 + width
        y2 = y1 + height
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= 'white', outline = "black", tags= 'C1')
        self.canvas2.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= 'white', outline = "black", tags= 'C2')
        self.canvas2.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C3')
        self.canvas2.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= 'white', outline = "black", tags= 'C4')
        self.canvas2.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= 'white', tags= 'CO')
        if self.diente_actual[8] == 'red' or self.diente_actual[8] == 'blue' or self.diente_actual[8] == 'green':
            self.canvas2.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.diente_actual[8], width= 5)
            self.canvas2.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.diente_actual[8], width= 5)
        for i in range (3, 10):
            if i != 8:
                self.diente_actual[i] = 'white'

    def restablecer_diente(self, numero):
        self.cargar_diente(numero)
        
    def cancelar(self):
        self.ventana_odontograma.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon= 'warning', parent= self.ventana_odontograma)
        if answer:            
            self.ventana_odontograma.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
            self.ventana_odontograma.focus_set() # Mantiene el foco cuando se abre la ventana.
            self.ventana_secundaria.destroy()
            self.canvas.delete("all")
            self.crear_dientes()
            self.ventana_odontograma.grab_set()
        else:
            self.ventana_odontograma.grab_set()

    def guardar_diente(self):
        self.ventana_secundaria.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea guardar?', icon= 'warning', parent= self.ventana_odontograma)
        if answer:
            try:
                self.miCursor = self.miConexion.cursor()
                #INSERT OR REPLACE INTO table(column_list) VALUES(value_list);
                sql = "INSERT INTO Dientes VALUES (NULL,?,?,?,?,?,?,?,?,?)"
                datos= self.diente_actual[1], self.ID_odonto+1, self.diente_actual[3], self.diente_actual[4], self.diente_actual[5], self.diente_actual[6], self.diente_actual[7], self.diente_actual[8], self.diente_actual[9]
                self.miCursor.execute(sql, datos)
                self.miConexion.commit()
                messagebox.showinfo("GUARDAR","Diente guardado exitosamente", parent= self.ventana_secundaria)                
                self.canvas.delete("all")
                self.cargar_dientes_modificados(self.ID_odonto+1)
                self.crear_dientes()
                self.ventana_secundaria.grab_set()
                self.ventana_secundaria.destroy()
                self.ventana_odontograma.grab_set()
            except:
                self.ventana_secundaria.grab_release()
                messagebox.showinfo("Diente", "No se pudieron guardar los cambios", parent= self.ventana_secundaria)
                self.ventana_odontograma.grab_set()
        else:
            self.ventana_secundaria.grab_set()
            
    def cargar_dientes_modificados(self, id_odonto):
        try:
            self.miCursor = self.miConexion.cursor()
            self.miCursor.execute("SELECT DISTINCT nro, nro_diente, id_odonto, d, v, m, i, o, extraccion, corona FROM dientes INNER JOIN Odontogramas ON dientes.id_odonto=Odontogramas.id_odontograma WHERE Odontogramas.dni_paciente=? AND dientes.id_odonto <=?\
                UNION SELECT * FROM dientes WHERE dientes.id_odonto =? ORDER by nro DESC", (self.dni_paciente, id_odonto, id_odonto, ))
            self.miConexion.commit()
            self.dientes= self.miCursor.fetchall()
        except:
            self.ventana_odontograma.grab_release()
            messagebox.showinfo("Dientes", "No se pudieron cargar dientes actuales", parent= self.ventana_odontograma)
            self.ventana_odontograma.grab_set()
            self.dientes=[]
            
    def cargar_dientes(self, id_odonto):
        if self.crear_odontograma:
            self.dientes=[]
        else:
            try:
                self.miCursor = self.miConexion.cursor()
                self.miCursor.execute("SELECT DISTINCT nro, nro_diente, id_odonto, d, v, m, i, o, extraccion, corona FROM dientes INNER JOIN Odontogramas ON dientes.id_odonto=Odontogramas.id_odontograma WHERE Odontogramas.dni_paciente=? AND dientes.id_odonto <=? ORDER BY dientes.id_odonto DESC", (self.dni_paciente, id_odonto,))            
                self.miConexion.commit()
                self.dientes= self.miCursor.fetchall()
            except:
                self.ventana_odontograma.grab_release()
                messagebox.showinfo("Dientes", "No se pudo cargar odontograma", parent= self.ventana_odontograma)
                self.ventana_odontograma.grab_set()

    def buscar_valor(self, valor):
        indice = 0
        try:
            for diente in self.dientes:
                if  diente[1] == valor:
                    return indice
                else:
                    indice+=1
        except ValueError:
            return None

    def change_cursor_enter(self, event):
        self.canvas.config(cursor= "hand2")

    def change_cursor_leave(self, event):
        self.canvas.config(cursor= "")

    def cambiar_color(self, event, numero, tag):
        if self.diente_actual[8] == 'white' and self.diente_actual[9] == 'white':
            item = self.canvas2.find_closest(event.x, event.y)
            current_color = self.canvas2.itemcget(item, "fill")
    # Cambiar el color del cuadrado según su estado actual
            if current_color == "white":
                self.canvas2.itemconfig(item, fill="red")
            elif current_color == "red":
                self.canvas2.itemconfig(item, fill="blue")
            elif current_color == "blue":
                self.canvas2.itemconfig(item, fill="green")
            elif current_color == "green":
                self.canvas2.itemconfig(item, fill="white")
            color_actual=self.canvas2.itemcget(item, "fill")
            if tag =='C1':
                if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
                    or numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
                    or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55\
                    or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85:
                    self.diente_actual[3]=color_actual
                elif numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
                    or numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
                    or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65 \
                    or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
                    self.diente_actual[5]=color_actual    
            if tag =='C2':
                if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
                    or numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
                    or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55\
                    or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65:
                    self.diente_actual[4]=color_actual
                elif numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
                    or numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
                    or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85 \
                    or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
                    self.diente_actual[6]=color_actual    
            if tag =='C3':
                if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
                    or numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
                    or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55\
                    or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85:
                    self.diente_actual[5]=color_actual
                elif numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
                    or numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
                    or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65 \
                    or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
                    self.diente_actual[3]=color_actual    
            if tag =='C4':
                if numero == 11 or numero == 12 or numero == 13 or numero == 14 or numero == 15 or numero == 16 or numero == 17 or numero == 18 \
                    or numero == 21 or numero == 22 or numero == 23 or numero == 24 or numero == 25 or numero == 26 or numero == 27 or numero == 28 \
                    or numero == 51 or numero == 52 or numero == 53 or numero == 54 or numero == 55\
                    or numero == 61 or numero == 62 or numero == 63 or numero == 64 or numero == 65:
                    self.diente_actual[6]=color_actual
                elif numero == 41 or numero == 42 or numero == 43 or numero == 44 or numero == 45 or numero == 46 or numero == 47 or numero == 48 \
                    or numero == 31 or numero == 32 or numero == 33 or numero == 34 or numero == 35 or numero == 36 or numero == 37 or numero == 38 \
                    or numero == 81 or numero == 82 or numero == 83 or numero == 84 or numero == 85 \
                    or numero == 71 or numero == 72 or numero == 73 or numero == 74 or numero == 75:
                    self.diente_actual[4]=color_actual 
            if tag =='CO':
                self.diente_actual[7]=color_actual

    def crear_dientes(self):
        width = 30
        height = 30
        padding = 10
        num_buttons = 8
        x1 = 10

        #primera hilera de dientes
        hilera1 = 18
        for _ in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height
            tag_diente = 'D' + str(hilera1)

            indice = self.buscar_valor(hilera1)

            self.texto1 = self.canvas.create_text(x1+ width/2, 15, text= hilera1, fill= "black", font= ('Helvetica 10 bold'))
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:                
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera1: self.editar_diente(numero))
            x1 = x2
            hilera1-=1

        #linea horizontal
        self.canvas.create_line(10, y2+padding, self.ancho-30, y2+padding, width= 2)
        x1 = x1+10
        #linea vertical
        self.canvas.create_line(x1, 0, x1, 270, width= 2)

        #2da hilera
        hilera2 = 21
        for i in range(num_buttons):
            x1 = x1 + padding
            y1 = 30
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera2)
            self.texto2= self.canvas.create_text(x1+ width/2, 15, text= hilera2, fill= "black", font= ('Helvetica 10 bold'))            
            tag_diente = 'D' + str(hilera2)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera2: self.editar_diente(numero))
            hilera2+=1
        y1 = y2+20
        x1 = 10

        #4ta hilera
        hilera4 = 48
        for i in range(num_buttons):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera4)
            self.texto4 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera4, fill= "black", font=('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera4)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera4: self.editar_diente(numero))
            hilera4-=1
        x1 = x1+10

        #3ra hilera
        hilera3 = 31
        for i in range(num_buttons):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera3)
            self.texto3 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera3, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera3)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera3: self.editar_diente(numero))
            hilera3+=1
        x1 = 130
        y1 = y2 + 60
        hilera5 = 55
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera5)
            self.texto5 = self.canvas.create_text(x1+ width/2, y1-15, text= hilera5, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera5)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera5: self.editar_diente(numero))
            hilera5-=1

        x1 = x2+11
        #y1= 195
        hilera6 = 61
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera6)
            self.texto6 = self.canvas.create_text(x1+ width/2, y1-15, text= hilera6, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera6)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")# MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera6: self.editar_diente(numero))
            hilera6+=1
        x1 = 130
        y1 = y2 + 10
        self.canvas.create_text(60, y2, text= 'DERECHA', fill= "black", font= ('Helvetica 10 bold'))
        self.canvas.create_text(x2+75, y2, text= 'IZQUIERDA', fill= "black", font= ('Helvetica 10 bold'))

        hilera8 = 85
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera8)
            tag_diente = 'D' + str(hilera8)
            self.texto8 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera8, fill= "black", font= ('Helvetica 10 bold'))

            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera8: self.editar_diente(numero))
            hilera8-=1
        x1 = x2+11
        y1 = y2-height
        hilera7 = 71
        for i in range(num_buttons-3):
            x1 = x1 + padding
            x2 = x1 + width
            y2 = y1 + height
            indice = self.buscar_valor(hilera7)
            self.texto3 = self.canvas.create_text(x1+ width/2, y2+15, text= hilera7, fill= "black", font= ('Helvetica 10 bold'))
            tag_diente = 'D' + str(hilera7)
            if(indice is not None):
                if self.dientes[indice][9] == 'red' or self.dientes[indice][9] == 'blue' or self.dientes[indice][9] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, width= 2, outline= self.dientes[indice][9])
                elif self.dientes[indice][8] == 'red' or self.dientes[indice][8] == 'blue' or self.dientes[indice][8] == 'green':
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
                    self.canvas.create_line(x1+5, y1+5, x2-5, y2-5, fill= self.dientes[indice][8], width= 2)
                    self.canvas.create_line(x1+5, y2-5, x2-5, y1+5, fill= self.dientes[indice][8], width= 2)
                else:
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= self.dientes[indice][5], outline = "black")#MEDIAL
                    self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= self.dientes[indice][6], outline = "black")#INTERIOR
                    self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][3], outline = "black")#DISTAL
                    self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= self.dientes[indice][4], outline = "black")#VESTIBULAR
                    self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= self.dientes[indice][7], tags= tag_diente)#OCLUSAL
            else:
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x1, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y1, x1 + width/2, y1 + height/2, x2, y1, fill= "white", outline = "black")
                self.canvas.create_polygon(x2, y1, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_polygon(x1, y2, x1 + width/2, y1 + height/2, x2, y2, fill= "white", outline = "black")
                self.canvas.create_rectangle(x1 + width/3.0, y1 + height/3.0, x2 - width/3.0, y2 - height/3.0, fill= "white", tags= tag_diente)
            x1 = x2
            self.canvas.tag_bind(tag_diente, '<Enter>', self.change_cursor_enter)
            self.canvas.tag_bind(tag_diente, '<Leave>', self.change_cursor_leave)
            self.canvas.tag_bind(tag_diente, '<Button-1>', lambda event, numero= hilera7: self.editar_diente(numero))
            hilera7+=1
        x1 = padding
        self.canvas.create_rectangle(100, y2+40, 150, y2+ 60, fill= "green")
        self.canvas.create_text(200, y2+50, text= 'Existentes', fill= "black", font= ('Helvetica 10 bold'))
        self.canvas.create_rectangle(300, y2+40, 350, y2+ 60, fill= "red")
        self.canvas.create_text(400, y2+50, text= 'Requeridas', fill= "black", font= ('Helvetica 10 bold'))
        self.canvas.create_rectangle(500, y2+40, 550, y2+ 60, fill= "blue")
        self.canvas.create_text(600, y2+50, text= 'Realizadas', fill= "black", font= ('Helvetica 10 bold'))

if __name__ == "__main__":
    Odontograma()