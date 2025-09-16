import tkinter as tk
from tkinter import ttk
import util.config as utl
from bd.conexion import Conexion
import re
from tkinter import messagebox, Button, Entry, Label, StringVar, Frame

class Usuario:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master_panel_ref = kwargs.get('master_panel_ref', None)
        self.nombre_usuario = StringVar()
        self.nombre_usuario_anterior = StringVar()
        self.clave = StringVar()
        self.tipo_usuario =  StringVar()
        self.id_usuario =  StringVar()
        self.usuario_existente = False
        self.fuenteb= utl.definir_fuente_bold()
        self.fuenten= utl.definir_fuente()
        self.color_fondo1, self.color_fondo2= utl.definir_color_fondo()
        self.db= Conexion()
        self.miConexion= self.db.conectar()
        self.miCursor= self.miConexion.cursor()

    def ventana(self, master_panel_ref=None):
        if master_panel_ref:
            self.master_panel_ref = master_panel_ref
        self.frame_usuario= tk.Toplevel()
        self.frame_usuario.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.frame_usuario.focus_set() # Mantiene el foco cuando se abre la ventana.
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.frame_usuario.iconphoto(False, self.imagen_ventana)
        self.frame_usuario.title('DentalMatic')
        self.frame_usuario.geometry('650x400')
        self.frame_usuario.config(bg= self.color_fondo2)
        self.frame_usuario.resizable(width= 0, height= 0)
        self.frame_usuario.columnconfigure(0, weight= 1)
        utl.centrar_ventana(self.frame_usuario, 650, 380)
        self.menu = True
        self.color = True
        self.frame_top = Frame(self.frame_usuario, bg= self.color_fondo1)
        self.frame_top.grid(column= 0, row= 0, columnspan= 3, sticky= "nsew")
        self.frame_principal = Frame(self.frame_usuario)
        self.frame_principal.config(bg= self.color_fondo2)
        self.frame_principal.grid(column= 1, row= 1, sticky= 'nsew')

        #Entradas Y ETIQUETAS DATOS DEL USUARIO
        Label(self.frame_principal, text= 'Nombre del usuario', anchor= "e", width= 20, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 1, pady= (20, 5))
        self.entry_nombre = Entry(self.frame_principal, textvariable= self.nombre_usuario, width= 25, font= self.fuenten)
        self.entry_nombre.grid(column= 1, row= 1, pady= 5, padx= 5)
        self.nombre_usuario_valido = Label(self.frame_principal, text= '*', anchor= 'w', width= 25, bg= self.color_fondo2, fg= 'red', font= self.fuenten)
        self.nombre_usuario_valido.grid(column= 2, row= 1, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Clave', anchor= "e", width= 20, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 2, pady= 5, padx= 2)
        self.entry_clave = Entry(self.frame_principal, textvariable= self.clave, width= 25, font= self.fuenten)
        self.entry_clave.grid(column= 1, row= 2, pady= 5, padx= 5)
        Label(self.frame_principal, text= '*', anchor= "w", width= 25, bg= self.color_fondo2, fg= 'red', font= self.fuenten).grid(column= 2, row= 2, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Tipo de usuario', anchor= "e", width= 20, bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 3, pady= 5, padx= 2)
        if(self.nombre_usuario.get()==''):
            self.titulo = Label(self.frame_top, text= 'Crear usuario', bg= self.color_fondo1, fg= 'white', font= self.fuenteb).grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Guardar', font= self.fuenteb, fg= 'white', bg= self.color_fondo1, activebackground= 'gray', bd= 2, width= 10, command= self.guardar).grid(column= 0, row= 6, pady= 5, padx= 5)
            self.combo=ttk.Combobox(self.frame_principal, textvariable= self.tipo_usuario, width= 23, font= self.fuenten, state= "readonly", values=["administrador", "odontologo", "secretario"])
            self.combo.grid(column= 1, row= 3, pady= 5, padx= 5)
            self.combo.current(2)
            self.combo.set("Elegir tipo usuario")
            Label(self.frame_principal, text= '*', anchor= "w", width= 25, bg= self.color_fondo2, fg= 'red', font= self.fuenten).grid(column= 2, row= 3, pady= 5, padx= 2)
        else:
            self.titulo = Label(self.frame_top, text= 'Actualizar usuario', bg= self.color_fondo1, fg= 'white', font= self.fuenteb).grid(column= 0, row= 0, pady= 20, padx= 10)
            Button(self.frame_principal, text= 'Actualizar',  font= self.fuenteb, fg= 'white', bg= self.color_fondo1, activebackground= 'gray', bd= 2, width= 10, command= self.actualizar).grid(column= 0, row= 6, pady= 5, padx= 5)
            self.combo=ttk.Combobox(self.frame_principal, textvariable= self.tipo_usuario, width= 23, font= self.fuenten, state= "disabled", values=["administrador", "odontologo", "secretario"])
            self.combo.grid(column= 1, row= 3, pady= 5, padx= 10)
        Label(self.frame_principal, text= '* Campos obligatorios', anchor= "w", width= 20, bg= self.color_fondo2, fg= 'red', font= self.fuenten).grid(column= 2, row= 4, pady= 5, padx= 2)

        Label(self.frame_principal, text= 'Contraseña: debe poseer un mínimo de 8 caracteres\n al menos una minuscula\n al menos una mayuscula\n al menos un digito', width= 50, borderwidth= 2, relief= "solid", bg= self.color_fondo2, fg= 'black', font= self.fuenten).grid(column= 0, columnspan= 3, row= 5, pady= 10)
        Button(self.frame_principal, text= 'Cerrar',  font= self.fuenteb, fg= 'white', bg= "orange", width= 10, command= self.Salir).grid(column= 2, row= 6, pady= 5, padx= (0, 10))
        self.frame_usuario.protocol("WM_DELETE_WINDOW", self.Salir)

        self.frame_usuario.mainloop()

    def guardar(self):        
        # Validar Formato del nombre de usuario
        if not self.validar_nombre(self.nombre_usuario.get()):
            self.frame_usuario.grab_release()
            messagebox.showinfo("Usuario inválido", "Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)", parent= self.frame_usuario)
            self.entry_nombre.config(bg= "orange red")
            self.frame_usuario.grab_set()
            return  # Sale si el formato no es válido

        # 2° Validación: Usuario único (que no exista previamente)
        if self.validar_usuario(self.nombre_usuario.get()):  # Si devuelve True, ya existe
            self.nombre_usuario_valido.config(text= "* Ya existe este usuario", fg= 'red')
            self.entry_nombre.config(bg= "orange red")
            return  # Sale si el usuario ya está registrado

        # 3° Validación: Contraseña (solo se verifica si las anteriores pasaron)
        if not self.validar_contrasenia(self.clave.get()):
            #messagebox.showinfo("Contraseña inválida", "La contraseña no cumple los requisitos")
            return  # Sale si la contraseña no es válida

        # 4° Validación: Tipo de usuario seleccionado
        if self.tipo_usuario.get() == "Elegir tipo usuario":
            self.frame_usuario.grab_release()            
            messagebox.showinfo("Tipo de usuario inválido", "Elija un tipo de usuario", parent= self.frame_usuario)
            self.frame_usuario.grab_set()
            return  # Sale si no se seleccionó tipo

        # Si todo es correcto, guarda en la base de datos
        datos = (self.nombre_usuario.get(), self.clave.get(), self.tipo_usuario.get())
        try:
            self.miCursor.execute("INSERT INTO Usuarios VALUES(NULL,?,?,?)", datos)
            self.miConexion.commit()
            if self.master_panel_ref:  # Si tenemos referencia al panel principal
                    self.master_panel_ref.mostrar_usuarios()
            self.db.cerrar_bd()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente", parent= self.frame_usuario)
            self.frame_usuario.destroy()            

        except Exception as e:
            self.frame_usuario.grab_release()
            messagebox.showerror("Error", f"No se pudo guardar. Error: {str(e)}", parent= self.frame_usuario)
            self.db.cerrar_bd()
            self.frame_usuario.grab_set()

    def cargar_datos(self, usuario):
        self.nombre_usuario.set(usuario)
        self.nombre_usuario_anterior=usuario
        try:
            self.miCursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=?", (usuario,))
            campos=self.miCursor.fetchone()
            self.clave.set(campos[2])
            self.tipo_usuario.set(campos[3])
        except:
            self.frame_usuario.grab_release()
            messagebox.showinfo("Buscar usuario", "No se ha podido cargar el usuario", parent= self.frame_usuario)
            self.frame_usuario.grab_set()

    def validar_usuario(self, nombre_usuario):
        try:
            self.miCursor.execute('SELECT COUNT(nombre_usuario) FROM usuarios WHERE nombre_usuario=?', (nombre_usuario,))
            existe = self.miCursor.fetchone()[0]
            self.usuario_existente = bool(existe)
        except:
            self.frame_usuario.grab_release()
            messagebox.showinfo("Usuario existente", "USUARIO EXISTENTE", parent= self.frame_usuario)
            self.frame_usuario.grab_set()
        return self.usuario_existente

    def actualizar(self):
        datos= self.clave.get(), self.nombre_usuario_anterior
        usuario_valido= False

        if not self.validar_nombre(self.nombre_usuario.get()):            
            self.frame_usuario.grab_release()   
            messagebox.showinfo("Usuario inválido", "Sólo letras o _ (Guión bajo)\nNo puede comenzar con _ (Guión bajo)", parent= self.frame_usuario)
            self.entry_nombre.config(bg= "orange red")
            self.frame_usuario.grab_set()
        elif self.validar_nombre(self.nombre_usuario.get()):
            self.entry_nombre.config(bg= "pale green")
            usuario_valido = True
        if self.validar_contrasenia(self.clave.get()) and usuario_valido:

            if self.nombre_usuario.get() == self.nombre_usuario_anterior:
                try:
                    sql="UPDATE usuarios SET pass_usuario=? where nombre_usuario=?"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    if self.master_panel_ref:  # Si tenemos referencia al panel principal
                        self.master_panel_ref.mostrar_usuarios()
                    self.frame_usuario.grab_release() 
                    messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente", parent= self.frame_usuario)
                    self.frame_usuario.grab_set()
                    self.frame_usuario.destroy()
                except:
                    self.frame_usuario.grab_release()
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario", parent= self.frame_usuario)
                    self.frame_usuario.grab_set()                 

            elif self.validar_usuario(self.nombre_usuario.get()):
                self.nombre_usuario_valido.config(text= "* Ya existe este usuario", fg= 'red')
                self.entry_nombre.config(bg= "orange red")
                pass
            else:
                datos=self.nombre_usuario.get(), self.clave.get(), self.nombre_usuario_anterior
                try:
                    sql="UPDATE usuarios SET nombre_usuario =?, pass_usuario=? where nombre_usuario=?"
                    self.miCursor.execute(sql, datos)
                    self.miConexion.commit()
                    if self.master_panel_ref:  # Si tenemos referencia al panel principal
                        self.master_panel_ref.mostrar_usuarios()
                    self.frame_usuario.grab_release()
                    messagebox.showinfo("GUARDAR","Usuario actualizado exitosamente", parent= self.frame_usuario)
                    self.frame_usuario.grab_set()
                    self.frame_usuario.destroy()
                except:
                    self.frame_usuario.grab_release()
                    messagebox.showinfo("GUARDAR", "No se ha podido guardar el usuario", parent= self.frame_usuario)
                    self.frame_usuario.grab_set()
                    return
        else:
            return

    def eliminar_usuario(self, nombre):
        msg_box = messagebox.askquestion('Eliminar usuario', '¿Desea elminar al usuario?', icon= 'warning')
        if msg_box == 'yes'and nombre != 'admin':
            try:
                self.miCursor.execute("DELETE FROM usuarios WHERE nombre_usuario = ?", (nombre,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Usuario eliminado exitosamente")
            except:
                messagebox.showinfo("ELIMINAR", "No se ha podido eliminar el usuario")

    def Salir(self):
        self.frame_usuario.grab_release()
        answer = messagebox.askokcancel('Salir', '¿Desea salir sin guardar?', icon= 'warning', parent= self.frame_usuario)
        self.frame_usuario.grab_set()
        #FUNCIONA
        if answer:
            self.miConexion.close()
            self.db.cerrar_bd()
            self.frame_usuario.destroy()

    # Mejor validación de nombre de usuario
    def validar_nombre(self, nombre_usuario):
        patron = r'^[a-zA-Z][a-zA-Z_]*$'  # Permite 1+ caracteres y _
        return bool(re.match(patron, nombre_usuario))

    # Validación de contraseña
    def validar_contrasenia(self, password):
        requisitos = [
            (len(password) >= 8, "Debe contener al menos 8 caracteres"),
            (any(c.isdigit() for c in password), "Agregar al menos un dígito"),
            (any(c.isupper() for c in password), "Agregar al menos una mayúscula"),
            (any(c.islower() for c in password), "Agregar al menos una minúscula")
        ]

        errores = [msg for (cumple, msg) in requisitos if not cumple]
        if errores:
            self.frame_usuario.grab_release()
            messagebox.showwarning("CONTRASEÑA INVÁLIDA", "\n".join(errores), parent= self.frame_usuario)
            self.frame_usuario.grab_set()
            self.entry_clave.config(bg="orange red")
            return False
        return True

if __name__ == "__main__":
    Usuario()