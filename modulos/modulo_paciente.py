from tkinter import *
import tkinter as tk
from tkinter.font import BOLD
import util.config as utl
from tkinter import messagebox, Button, Entry, Label
from tkinter import  StringVar, Frame
import re
from datetime import datetime
from bd.conexion import Conexion
#from bd.conexion import Conexion
#import sqlite3


class Paciente:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master_panel_ref = kwargs.get('master_panel_ref', None)
        self.nombre_paciente = StringVar()
        self.apellido_paciente = StringVar()
        self.dni_paciente_anterior =  StringVar()
        self.dni_paciente =  StringVar()
        self.nacimiento_paciente =  StringVar(value= 'Formato: DD-MM-AAAA')
        self.edad_paciente =  StringVar()
        self.domicilio_paciente =  StringVar()
        self.telefono_paciente =  StringVar()
        self.email_paciente =  StringVar()
        self.obrasocial_paciente =  StringVar()
        self.nrosocio_paciente =  StringVar()
        #self.correovalido=False
        self.color_fondo1, self.color_fondo2 = utl.definir_color_fondo()
        self.fuenteb= utl.definir_fuente_bold()
        self.fuenten= utl.definir_fuente()
        self.ancho= 20
        self.db = Conexion()
        self.miConexion= self.db.conectar()
        self.miCursor= self.miConexion.cursor()

    def ventana_paciente(self, master_panel_ref=None):
        if master_panel_ref:
            self.master_panel_ref = master_panel_ref
        self.frame_paciente= tk.Toplevel()
        self.frame_paciente.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_paciente.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_paciente.iconphoto(False, self.imagen_ventana)
        self.frame_paciente.title('DentalMatic')
        self.frame_paciente.geometry('800x300')
        self.frame_paciente.config(bg= 'gray90')
        self.frame_paciente.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.frame_paciente, 700, 500)
        self.menu = True
        self.color = True

        self.frame_top = Frame(self.frame_paciente, bg= self.color_fondo1, height= 50)
        self.frame_top.grid(column= 1, row= 0, sticky= 'ew')
        self.titulo = Label(self.frame_top, text= 'Datos del paciente', bg= self.color_fondo1, fg= 'white', font= self.fuenteb)
        self.titulo.grid(column= 0, row= 0, pady= 20, padx= 10)

        self.frame_principal = Frame(self.frame_paciente)
        self.frame_principal.config(bg= 'gray90')
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')

        #Entradas Y ETIQUETAS DATOS DEL PACIENTE
        #NOMBRE
        Label(self.frame_principal, text= 'Nombre/s', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 1, pady= 5, padx= 2)
        self.entry_nombre = Entry(self.frame_principal, textvariable= self.nombre_paciente, width= 25, font= self.fuenten)
        self.entry_nombre.grid(column= 1, row= 1, pady= 5)
        self.nombre_valido = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.nombre_valido.grid(column= 2, row= 1, pady= 5)

        #APELLIDO
        Label(self.frame_principal, text= 'Apellido/s', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 2, pady= 5, padx= 2)
        self.entry_apellido = Entry(self.frame_principal, textvariable= self.apellido_paciente, width= 25, font= self.fuenten)
        self.entry_apellido.grid(column= 1, row= 2, pady= 5)
        self.apellido_valido = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.apellido_valido.grid(column= 2, row= 2, pady= 5)

        #DNI
        Label(self.frame_principal, text= 'D.N.I.', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 3, pady= 5, padx= 2)
        self.entry_dni = Entry(self.frame_principal, textvariable= self.dni_paciente, width= 25, font= self.fuenten)
        self.entry_dni.grid(column= 1, row= 3, pady= 5)
        self.dni_valido = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.dni_valido.grid(column= 2, row= 3, pady= 5)

        #Fecha de nacimiento
        Label(self.frame_principal, text= 'Fecha de nacimiento', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 4, pady= 5, padx= 2)
        self.entry_fecha = Entry(self.frame_principal, textvariable= self.nacimiento_paciente, width= 25, font= self.fuenten)
        self.entry_fecha.grid(column= 1, row= 4, pady= 5)
        self.entry_fecha.bind("<FocusIn>", self.seleccionar_todo)
        self.fecha_valida = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.fecha_valida.grid(column= 2, row= 4, pady= 5)

        #EDAD
        Label(self.frame_principal, text= 'Edad', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 5, pady= 5, padx= 2)
        self.entry_edad = Entry(self.frame_principal, textvariable= self.edad_paciente, width= 25, font= self.fuenten, state='disabled')
        self.entry_edad.grid(column= 1, row= 5, pady= 5)

        #DOMICILIO
        Label(self.frame_principal, text= 'Domicilio', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 6, pady= 5, padx= 2)
        self.entry_domicilio = Entry(self.frame_principal, textvariable= self.domicilio_paciente, width= 25, font= self.fuenten)
        self.entry_domicilio.grid(column= 1, row= 6, pady= 5)
        self.domicilio_valido = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.domicilio_valido.grid(column= 2, row= 6, pady=5)

        #TELEFONO
        Label(self.frame_principal, text= 'Telefono', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 7, pady= 5, padx= 2)
        self.entry_telefono = Entry(self.frame_principal, textvariable= self.telefono_paciente, width= 25, font= self.fuenten)
        self.entry_telefono.grid(column= 1, row= 7, pady= 5)
        self.telefono_valido = Label(self.frame_principal, text= '*', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.telefono_valido.grid(column= 2, row= 7, pady=5)

        #CORREO ELECTRONICO
        Label(self.frame_principal, text= 'Email', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 8, pady= 5, padx= 2)
        self.entry_correo = Entry(self.frame_principal, textvariable= self.email_paciente, width= 25, font= self.fuenten)
        self.entry_correo.grid(column= 1, row= 8, pady= 5)
        validate_email = self.frame_principal.register(lambda email: self.validar_email(self.entry_correo))
        self.entry_correo.config(validate= "key", validatecommand= (validate_email, '%P'))
        def actualizar_label(event):
            self.validar_email(self.entry_correo)
        self.entry_correo.bind('<Key>', actualizar_label)
        self.email_valido_label = Label(self.frame_principal, text= '', anchor= "w", width= 30, bg= 'gray90', fg= 'red', font= self.fuenten)
        self.email_valido_label.grid(column= 2, row= 8, pady= 5)

        #OBRA SOCIAL
        Label(self.frame_principal, text= 'Obra Social', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 9, pady= 5, padx= 2)
        self.entry_obrasocial = Entry(self.frame_principal, textvariable= self.obrasocial_paciente, width= 25, font= self.fuenten)
        self.entry_obrasocial.grid(column= 1, row= 9, pady= 5)

        #NUMERO DE SOCIO
        Label(self.frame_principal, text= 'Nro de socio', bg= 'gray90', fg= 'black', anchor= "e", width= self.ancho, font= self.fuenteb).grid(column= 0, row= 10, pady= 5, padx= 2)
        self.entry_nrosocio = Entry(self.frame_principal, textvariable= self.nrosocio_paciente, width= 25, font= self.fuenten)
        self.entry_nrosocio.grid(column= 1, row= 10, pady= 5)

        Label(self.frame_principal, text= '* Campos obligatorios', anchor= "e", width= 20, bg= 'gray90', fg= 'red', font= self.fuenten).grid(column= 2, row= 11, pady= 5, padx= 2)

       #BOTONES GUARDAR Y CERRAR
        if(self.dni_paciente.get()==''):
            Button(self.frame_principal, text= 'Guardar', font= self.fuenteb, fg= 'white', bg= self.color_fondo1, activebackground= 'gray', width=15, bd= 2, command= self.guardar).grid(column= 0, row=12, pady= 5, padx= 20)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar paciente', bg= self.color_fondo1, fg= 'white', font= self.fuenteb).grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar', font= self.fuenteb, fg= 'white', bg= self.color_fondo1, width= 15, activebackground= 'gray', bd= 2, command= self.actualizar).grid(column= 0, row= 12, pady= 5, padx= 20)
        Button(self.frame_principal, text= 'Cerrar', font= self.fuenteb, fg= 'white', bg= 'orange', activebackground= 'gray', width= 15, bd= 2, command= self.Salir).grid(column= 2, row= 12, pady= 5)

        self.frame_paciente.mainloop()
    
    def seleccionar_todo(self, event):
        event.widget.select_range(0, tk.END)
        event.widget.icursor(tk.END)
    
    def validar_email(self, email):
        email = self.entry_correo.get()
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.entry_correo.config(bg= "pale green")
            self.email_valido_label.config(text= "Formato válido", fg= 'green')
            #self.correovalido = True
        else:
            self.entry_correo.config(bg= "orange red")
            self.email_valido_label.config(text= "Formato inválido", fg= 'red')
            #self.correovalido = False

    def validar_dni(self, dni):
        if len(dni) > 8:
            return False
        return dni.isdecimal()

    def validar_fecha(self, fecha):
        regex_fecha = r"^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$"
        if re.match(regex_fecha, fecha):
            return True
        else:
            return False
    
    def convertir_fecha(self, fecha):
        fecha_obj = datetime.strptime(fecha, "%d-%m-%Y")
        # Convertir el objeto datetime al formato deseado (aaaa-mm-dd)
        self.fecha_transformada = fecha_obj.strftime("%Y-%m-%d")        
        return self.fecha_transformada 

    def calcular_edad(self, fecha_nacimiento_str):
        try:
            # Validar formato de fecha primero
            if not self.validar_fecha(fecha_nacimiento_str):
                raise ValueError("Formato de fecha inválido")

            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%d-%m-%Y")
            fecha_actual = datetime.now()

            # Calcular edad
            edad = fecha_actual.year - fecha_nacimiento.year

            # Ajustar si aún no ha cumplido años este año
            if (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1

            # Validar rangos de edad razonables
            if edad < 0:
                raise ValueError("La fecha de nacimiento no puede ser futura")
            if edad > 120:
                raise ValueError("Edad improbable, verifique la fecha")

            self.edad_paciente.set(str(edad))
            return edad

        except ValueError as e:
            self.edad_paciente.set("")
            self.fecha_valida.config(text= f"* Error: {str(e)}", fg= 'red')
            self.entry_fecha.config(bg= "orange red")
            return None

    def validar_alfanum(self, texto):
        if texto == '':
            return False
        for char in texto:
            if not (char.isalnum() or char.isspace()):
                return False
        return True

    def validar_telefono(self, telefono):
        if len(telefono) > 11:
            return False
        return telefono.isdecimal()

    def validar_alfa(self, texto):
        if texto == '':
            return False
        for char in texto:
            if not (char.isalpha() or char.isspace()):
                return False
        return True

    def cargar_datos(self, dni):
        self.dni_paciente_anterior= dni
        try:
            self.miCursor.execute("SELECT * FROM Pacientes WHERE ID=?", (dni,))
            campos=self.miCursor.fetchall()
            self.dni_paciente.set(dni)
            self.nombre_paciente.set(campos[0][1])
            self.apellido_paciente.set(campos[0][2])
            self.domicilio_paciente.set(campos[0][3])
            self.telefono_paciente.set(campos[0][4])
            self.email_paciente.set(campos[0][5])
            self.obrasocial_paciente.set(campos[0][6])
            self.nrosocio_paciente.set(campos[0][7])
            self.edad_paciente.set(campos[0][8])
            fecha_obj = datetime.strptime(campos[0][9], "%Y-%m-%d")
            fecha_date = fecha_obj.date()            
            self.nacimiento_paciente.set(fecha_date.strftime("%d-%m-%Y"))
        except:
            self.frame_paciente.grab_release()
            messagebox.showinfo("Buscar paciente", "No se ha podido encontrar el paciente", parent= self.frame_paciente)
            self.frame_paciente.grab_set()

    def completar_campos(self):
        campos_vacios= True
        if(self.nombre_paciente.get()==''):
            self.nombre_valido.config(text= "* Complete este campo", fg= 'red')
            self.entry_nombre.config(bg= "orange red")
            campos_vacios= False
        if(self.apellido_paciente.get()==''):
            self.apellido_valido.config(text= "* Complete este campo", fg= 'red')
            self.entry_apellido.config(bg= "orange red")
            campos_vacios= False
        if(self.dni_paciente.get()==''):
            self.dni_valido.config(text= "* Complete este campo", fg= 'red')
            self.entry_dni.config(bg= "orange red")
            campos_vacios= False
        if(self.nacimiento_paciente.get()==''):
            self.fecha_valida.config(text= "* Complete este campo", fg= 'red')
            self.entry_fecha.config(bg= "orange red")
            campos_vacios= False
        if(self.domicilio_paciente.get()==''):
            self.domicilio_valido.config(text= "* Complete este campo", fg= 'red')
            self.entry_domicilio.config(bg= "orange red")
            campos_vacios= False
        if(self.telefono_paciente.get()==''):
            self.telefono_valido.config(text= "* Complete este campo", fg= 'red')
            self.entry_telefono.config(bg= "orange red")
            campos_vacios= False
        if(self.email_paciente.get()==''):
            self.email_valido_label.config(text= "* Complete este campo", fg= 'red')
            self.entry_correo.config(bg= "orange red")
            campos_vacios= False
        return campos_vacios    

    def validar_datos(self):
        campos_validos = True
        if not self.validar_alfa(self.nombre_paciente.get()):
            self.nombre_valido.config(text= "* Sólo letras", fg= 'red')
            self.entry_nombre.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_nombre.config(bg= "pale green")
            self.nombre_valido.config(text= "*", fg= 'red')

        if not self.validar_alfa(self.apellido_paciente.get()):
            self.apellido_valido.config(text= "* Sólo letras", fg= 'red')
            self.entry_apellido.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_apellido.config(bg= "pale green")
            self.apellido_valido.config(text= "*", fg= 'red')

        if not self.validar_dni(self.dni_paciente.get()):
            self.dni_valido.config(text= "* Sólo números, hasta 8 dígitos", fg= 'red')
            self.entry_dni.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_dni.config(bg= "pale green")
            self.dni_valido.config(text= "*", fg= 'red')

        if not self.validar_fecha(self.nacimiento_paciente.get()):
            self.fecha_valida.config(text= "* Formato: DD-MM-AAAA", fg= 'red')
            self.entry_fecha.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_fecha.config(bg= "pale green")
            self.fecha_valida.config(text= "*", fg= 'red')

        if not self.validar_alfanum(self.domicilio_paciente.get()):
            self.domicilio_valido.config(text= "* Sólo letras y/o números", fg= 'red')
            self.entry_domicilio.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_domicilio.config(bg= "pale green")
            self.domicilio_valido.config(text= "*", fg= 'red')

        if not self.validar_telefono(self.telefono_paciente.get()):
            self.telefono_valido.config(text= "* Sólo números, hasta 11 dígitos", fg= 'red')
            self.entry_telefono.config(bg= "orange red")
            campos_validos= False
        else:
            self.entry_telefono.config(bg= "pale green")
            self.telefono_valido.config(text= "*", fg='red')

        return campos_validos    

    def actualizar(self):        
        if self.completar_campos() and self.validar_datos():
            self.calcular_edad(self.nacimiento_paciente.get())
            fecha = self.convertir_fecha(self.nacimiento_paciente.get()) 

            datos=self.dni_paciente.get(), self.nombre_paciente.get().upper(), self.apellido_paciente.get().upper(), self.domicilio_paciente.get().upper(), self.telefono_paciente.get(),\
                self.email_paciente.get(), self.obrasocial_paciente.get().upper(), self.nrosocio_paciente.get(), self.edad_paciente.get(), fecha, self.dni_paciente_anterior
            try:
                sql="UPDATE Pacientes SET ID=?, nombre =?, apellido=?,  domicilio=?, telefono=?, email=?, obrasocial=?, nrosocio=?, edad=?, fechanacimiento=? where ID=?"
                self.miCursor.execute(sql, datos)
                self.miConexion.commit()
                if self.master_panel_ref:  # Si tenemos referencia al panel principal
                    self.master_panel_ref.mostrar_pacientes()
                self.frame_paciente.grab_release()
                messagebox.showinfo("GUARDAR","Paciente actualizado exitosamente", parent= self.frame_paciente)
                self.frame_paciente.destroy()
            except:
                self.frame_paciente.grab_release()
                messagebox.showinfo("GUARDAR", "No se ha podido actualizar el paciente", parent= self.frame_paciente)
                self.frame_paciente.grab_set()

    def dni_existe(self, dni):
        """Verifica si un DNI ya existe en la base de datos"""
        self.miCursor.execute("SELECT 1 FROM Pacientes WHERE ID=?", (dni,))
        return self.miCursor.fetchone() is not None

    def guardar(self):
        # Primero validar campos y datos
        if not (self.completar_campos() and self.validar_datos()):
            return

        # Verificar si el DNI ya existe
        dni = self.dni_paciente.get()
        if self.dni_existe(dni):
            messagebox.showwarning("DNI Existente", 
                                f"Ya existe un paciente registrado con el DNI {dni}.\n"
                                "Verifique los datos o utilice la opción 'Actualizar'.")
            self.entry_dni.config(bg= "orange red")
            self.dni_valido.config(text= "* DNI ya registrado", fg= 'red')
            self.entry_dni.focus_set()  # Coloca el foco en el campo DNI
            return

        # Si todo está bien, proceder con el guardado
        self.calcular_edad(self.nacimiento_paciente.get())
        fecha = self.convertir_fecha(self.nacimiento_paciente.get())            
        datos = (
            dni,
            self.nombre_paciente.get().upper(),
            self.apellido_paciente.get().upper(),
            self.domicilio_paciente.get().upper(),
            self.telefono_paciente.get(),
            self.email_paciente.get(),
            self.obrasocial_paciente.get().upper(),
            self.nrosocio_paciente.get(),
            self.edad_paciente.get(),
            fecha
        )

        try:
            self.miCursor.execute("INSERT INTO Pacientes VALUES(?,?,?,?,?,?,?,?,?,?)", datos)
            self.miConexion.commit()
            if self.master_panel_ref:  # Si tenemos referencia al panel principal
                self.master_panel_ref.mostrar_pacientes()
            self.frame_paciente.grab_release()
            messagebox.showinfo("Éxito", "Paciente guardado exitosamente", parent= self.frame_paciente)
            self.frame_paciente.destroy()
        except Exception as e:
            self.frame_paciente.grab_release()
            messagebox.showerror("Error", f"No se pudo guardar el paciente. Error: {str(e)}", parent= self.frame_paciente)
            self.frame_paciente.grab_set()

    def Salir(self):
        self.frame_paciente.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon='warning', parent= self.frame_paciente)
        if answer:            
            self.frame_paciente.destroy()
        else:
            self.frame_paciente.grab_set()

if __name__ == "__main__":
    Paciente()