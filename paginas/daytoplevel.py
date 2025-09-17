import util.config as utl
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from datetime import *
#import sqlite3
from tkinter import Button
from paginas.datehandler import DateHandler
from bd.conexion import Conexion
import re

class DayTopWindow(Toplevel):

    def __init__(self, dia: int, mes: int, anio: int):
        super().__init__()

        self.attributes = ("-topmost", True)
        utl.centrar_ventana(self, 800, 610)
        self.title("Agenda de turnos")
        self.resizable(width= True, height= False)
        self.turnos_box = None
        self.configure(bg= "#D1D6D3")
        self.grab_set_global()
        self.focus_set()
        self.extension = None
        self.confirmation = None
        self.fuenten= utl.definir_fuente()
        self.fuenteb= utl.definir_fuente_bold()
        self.db = Conexion()
        self.conn= self.db.conectar()

        self.dia = dia
        self.mes = mes
        self.anio = anio

        self.crear_encabezado()
        self.crear_botones_cambio_fecha()
        self.cargar_odontologos()
        self.crear_lista_turnos()
        self.cargar_turnos()

    def crear_encabezado(self):
        """ Crea encabezado """
        encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado = Label(self, text= encabezado_texto, font= "Arial 15", justify= CENTER, borderwidth= 3, bd= 3, bg= "#D1D6D3")
        self.encabezado.grid(row= 0, column= 1, ipady= 3)

    def configurar_encabezado(self):
        """ Actualiza el header de la fecha """
        self.encabezado_texto = f"{self.dia}/{self.mes}/{self.anio}"
        self.encabezado.configure(text= self.encabezado_texto)

    def crear_botones_cambio_fecha(self):
        """ Crea botones para cambiar fecha """
        Button(self, text= ">", command= self.avanzar_dia,fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 2)
        Button(self, text= "<", command= self.retroceder_dia, fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, width= 5).grid(row= 0, column= 0)
        Button(self, text= "Salir", font= self.fuenteb, fg= 'white', bg= "orange", width= 8, command= self.destroy).grid(row= 0, column= 3, pady= (5,5))

    def crear_lista_turnos(self):
        estilo_tabla2 = ttk.Style(self)
        estilo_tabla2.theme_use("alt")
        estilo_tabla2.configure("TablaTurnos.Treeview", font= self.fuenten, foreground= 'black', rowheight= 20)
        estilo_tabla2.configure('TablaTurnos.Treeview.Heading', background= '#1F704B', foreground= 'white', padding= 3, font= self.fuenteb)
        self.frame_tabla = ttk.Frame(self)
        self.frame_tabla.grid(column= 0, columnspan= 4, row= 2, sticky= 'nsew')
        self.tabla_turnos = ttk.Treeview(self.frame_tabla, columns= ("Horario", "Paciente", "Prestacion", "Odontologo"), show= 'headings', height= 25, selectmode ='browse', style="TablaTurnos.Treeview")
        self.tabla_turnos.grid(column= 0, row= 2, columnspan= 4, sticky= 'nsew', padx= 5, pady= 5)
        [self.frame_tabla.columnconfigure(i, weight= 1) for i in range(self.grid_size()[0])]
        [self.columnconfigure(i, weight= 1) for i in range(self.grid_size()[0])]
        [self.frame_tabla.rowconfigure(i, weight= 1) for i in range(self.grid_size()[1])]
        [self.rowconfigure(i, weight= 1) for i in range(self.grid_size()[1])]

        # Definir los encabezados de las columnas
        self.tabla_turnos.heading("Horario", text= "Horario")
        self.tabla_turnos.heading("Paciente", text= "Paciente")
        self.tabla_turnos.heading("Prestacion", text= "Prestacion")
        self.tabla_turnos.heading("Odontologo", text= "Odontologo")

        # Ajustar el ancho de las columnas
        self.tabla_turnos.column("Horario", width= 70, anchor= 'center')
        self.tabla_turnos.column("Paciente", width= 200)
        self.tabla_turnos.column("Prestacion", width= 250)
        self.tabla_turnos.column("Odontologo", width= 200)

        self.tabla_turnos.bind("<ButtonRelease-1>", self.editar_turno)

    def cargar_turnos(self):
        start_date = date(self.anio, self.mes, self.dia)
        self.cur= self.conn.cursor()
        try:
            self.cur.execute("SELECT Turnos.Hora, Turnos.Paciente, Odontologos.Apellido_odontologo, Odontologos.Nombre_odontologo, Turnos.Prestacion FROM Odontologos JOIN Turnos ON Odontologos.Matricula = Turnos.Odontologo WHERE Turnos.Fecha=? ORDER BY Turnos.Hora", (start_date,))
            self.turnos_dados = self.cur.fetchall()
            self.conn.commit()
        except:
            self.grab_release()
            messagebox.showinfo("Turnos", "No hay turnos", parent= self)
            self.grab_set()

        start_time = datetime.strptime("08:00", "%H:%M")
        # Intervalo de 30 minutos
        time_interval = timedelta(minutes= 30)
        self.j = 0
        self.tabla_turnos.delete(*self.tabla_turnos.get_children())
        for i in range(0, 25):
            current_time = start_time + i * time_interval
            if not self.turnos_dados:
                self.tabla_turnos.insert(parent= '', index= 'end', values=(current_time.strftime("%H:%M"), '', '', ''))
            else:
                if(current_time.strftime("%H:%M") == self.turnos_dados[self.j][0] and self.j < len(self.turnos_dados)):
                    
                    self.tabla_turnos.insert("", "end", values=(current_time.strftime("%H:%M"), self.turnos_dados[self.j][1], self.turnos_dados[self.j][4], self.turnos_dados[self.j][2]+", "+self.turnos_dados[self.j][3]), tags=('anotado',))
                    self.tabla_turnos.tag_configure('anotado', font= self.fuenteb, background="green")
                    if(self.j+1 < len(self.turnos_dados)):
                        self.j=self.j+1
                else:
                    self.tabla_turnos.insert(parent= '', index= 'end', values=(current_time.strftime("%H:%M"), '', '', ''))
            self.tabla_turnos.tag_configure('anotado', font= self.fuenteb, background= "green")

    def editar_turno(self, event):
        region = self.tabla_turnos.identify("region", event.x, event.y)
        if region == "heading":  # Si el doble clic es en el encabezado
            messagebox.showwarning("Advertencia", "Debe seleccionar un horario")
            return
        self.ventana_secundaria = tk.Toplevel(self, background= 'gray')
        self.ventana_secundaria.title("Turno")
        self.ventana_secundaria.geometry('400x300')
        utl.centrar_ventana(self.ventana_secundaria, 400, 290)
        self.ventana_secundaria.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.ventana_secundaria.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.cur= self.conn.cursor()
        self.turno_seleccionado = self.tabla_turnos.selection()[0]
        self.data = self.tabla_turnos.item(self.turno_seleccionado)
        odontologo= ''
        self.horario = self.data['values'][0]
        self.paciente = self.data['values'][1]
        self.prestacion = self.data['values'][2]
        odontologo = self.data['values'][3]

        try:
            fecha_turno = date(self.anio, self.mes, self.dia)
            self.cur.execute("SELECT Odontologo FROM turnos WHERE fecha= ? AND hora= ?", (fecha_turno, self.horario,))
            matricula = self.cur.fetchone()
            self.cur.execute("SELECT Apellido_odontologo, Nombre_odontologo FROM Odontologos WHERE Matricula= ? ", (matricula))
            odontologo = self.cur.fetchone()
        except:
            pass
        if self.paciente == '':
            Label(self.ventana_secundaria, text= "GUARDAR TURNO", font= ("Arial", 15, 'bold'), bg= "gray90", width= 60).pack(pady= 5)
        else:
            Label(self.ventana_secundaria, text= "EDITAR TURNO", font= ("Arial", 15, 'bold'), bg= "gray90", width= 60).pack(pady= 5)
        
        Label(self.ventana_secundaria, text= f"FECHA: {self.dia}/{self.mes}/{self.anio} - HORARIO: "+self.horario, font= ("Arial", 13, 'bold'), bg= "gray90", width= 60).pack(pady= 5)

        self.nombre_entry = Entry(self.ventana_secundaria, width= 42, justify= CENTER)
        self.nombre_entry.pack(pady= (20,10))
        self.nombre_entry.insert(0, "Paciente")
        if (self.paciente != ''):
            self.nombre_entry.delete(0, END)
            self.nombre_entry.insert(0, self.paciente)
        self.nombre_entry.focus_set()
        prestaciones = ["CONSULTA", "EXTRACCIÓN", "TRATAMIENTO DE CONDUCTO", "LIMPIEZA"]
        self.selector_prestacion = ttk.Combobox(self.ventana_secundaria, state= "readonly", values= prestaciones, width= 40, justify= CENTER, background= "white")
        self.selector_prestacion.pack(pady= 8)
        self.selector_prestacion.set("Prestación")
        if (self.prestacion != ''):
            self.selector_prestacion.set(self.prestacion)
        self.selector_prestacion.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())
        self.selector_odontologo= ttk.Combobox(self.ventana_secundaria, values= self.valores_combobox, state= "readonly", width= 40, justify= CENTER, background= "white")
        self.selector_odontologo.pack(pady= 8)
        self.selector_odontologo.set("Odontólogo")
        if self.valores_combobox == []:
            self.selector_odontologo.set("No hay odontologos")
        if odontologo != '':
            profesional = f"Mat. {matricula[0]} - {odontologo[0]}, {odontologo[1]}"
            self.selector_odontologo.set(profesional)
        self.selector_odontologo.bind("<<ComboboxSelected>>", lambda e: self.ventana_secundaria.focus())

        self.button_frame = Frame(self.ventana_secundaria, bg= "gray")
        self.button_frame.pack(pady= (30, 0))

        Button(self.button_frame, text= 'Guardar', command= self.guardar_turno, font= self.fuenteb, fg= 'white', bg= "green", width= 10).grid(row= 0, column= 0, padx= 10)
        self.boton_eliminar= Button(self.button_frame, text= 'Eliminar', command= self.eliminar_turno, font= self.fuenteb, fg= 'white', bg= "red", width= 10)
        self.boton_eliminar.grid(row= 0, column= 1, padx= 10)
        if self.nombre_entry.get() == 'Paciente':
            self.boton_eliminar["state"] = DISABLED
        Button(self.button_frame, text= 'Salir', command= self.cancelar_turno, font= self.fuenteb, fg= 'white', bg= "orange", width= 10).grid(row= 0, column= 2, padx= 10)

    def cancelar_turno(self):
        self.ventana_secundaria.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon='warning', parent= self.ventana_secundaria)
        if answer:
            self.grab_set_global()
            self.focus_set()            
            self.ventana_secundaria.destroy()
        else:
            self.ventana_secundaria.grab_set()

    def eliminar_turno(self):
        start_date = date(self.anio, self.mes, self.dia)
        self.cur= self.conn.cursor()
        hora= self.horario
        self.ventana_secundaria.grab_release()
        answer = messagebox.askokcancel('Eliminar', '¿Desea eliminar el turno?', icon='warning', parent= self.ventana_secundaria)
        if answer:
            try:
                self.cur.execute("DELETE FROM turnos WHERE fecha= ? AND hora= ?", (start_date, hora,))
                self.conn.commit()
                self.grab_set_global()
                self.focus_set()
                self.ventana_secundaria.destroy()
            except:
                messagebox.showerror("Eliminar", "No se pudo eliminar", parent= self.ventana_secundaria)
                self.ventana_secundaria.grab_set()
        else:
            self.ventana_secundaria.grab_set()
        self.cargar_turnos()

    def guardar_turno(self):
        """El día se carga en formato YYYY/MM/DD para luego poder usar los métodos de SQLite"""
        start_date= date(self.anio, self.mes, self.dia)
        self.conn=  self.db.conectar()
        self.cur= self.conn.cursor()
        self.matricula= ""
        self.matricula = self.obtener_matricula_odontologo()
        self.ventana_secundaria.grab_release()
        if self.nombre_entry.get().upper() == "PACIENTE":
            messagebox.showerror("Paciente", "Ingrese nombre paciente", parent= self.ventana_secundaria)
            self.ventana_secundaria.grab_set()
            return
        elif self.selector_prestacion.get().upper() == "PRESTACIÓN":
            messagebox.showerror("Prestación", "Elija la prestación", parent= self.ventana_secundaria)
            self.ventana_secundaria.grab_set()
            return
        elif self.selector_odontologo.get().upper() == "ODONTÓLOGO":
            messagebox.showerror("Odontólogo", "Elija odontólogo", parent= self.ventana_secundaria)
            self.ventana_secundaria.grab_set()
            return
        else:
            datos = start_date, self.horario, self.nombre_entry.get().upper(), self.matricula, self.selector_prestacion.get().upper()
            answer = messagebox.askokcancel('Guardar', '¿Desea guardar el turno?', icon='warning', parent= self.ventana_secundaria)
            if answer:
                try:
                    sql="REPLACE INTO turnos VALUES(?, ?, ?, ?, ?)"
                    self.cur.execute(sql, datos)
                    self.conn.commit()
                    self.ventana_secundaria.destroy()
                    self.grab_set()
                    self.cargar_turnos()
                except:
                    messagebox.showerror("Guardar", "No se pudo guardar", parent= self.ventana_secundaria)

    def obtener_matricula_odontologo(self):
        """Extrae la matrícula del odontólogo seleccionado"""
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

    def cargar_odontologos(self):
        self.cur= self.conn.cursor()
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
            self.ventana_secundaria.grab_release()
            messagebox.showinfo("Odontologos", "No hay odontologos cargados", parent= self.ventana_secundaria)
            self.ventana_secundaria.grab_set()

    def avanzar_dia(self):
        """ AVANZAR 1 DIA """
        cant_dias = DateHandler().days_in_month(self.mes, self.anio)
        self.dia += 1
        if self.dia > cant_dias:
            self.dia = 1
            self.mes += 1
            if self.mes > 12:
                self.mes = 1
                self.anio += 1
        self.configurar_encabezado()
        self.cargar_turnos()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def retroceder_dia(self):
        """ RETROCEDER 1 DIA """
        self.dia -= 1
        if self.dia < 1:
            self.mes -= 1
            if self.mes < 1:
                self.anio -= 1
            self.dia = DateHandler().days_in_month(self.mes, self.anio)
        self.configurar_encabezado()
        self.cargar_turnos()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None