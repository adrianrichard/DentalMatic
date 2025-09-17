import tkinter as tk
import sqlite3
import util.config as utl
from tkinter import  Button, messagebox, Label, ttk, PhotoImage
from tkinter import  StringVar, Frame
import os
import sys
import subprocess
import time
from modulos.modulo_paciente import Paciente
from modulos.modulo_usuario import Usuario
from modulos.modulo_odontologo import Odontologo
from paginas.calendario import Calendario
from paginas.odontograma import Odontograma
from paginas.informes import Informes
from paginas.galeria import Galeria
from bd.backup import Backup
#from util.visorimagenes import ImageGalleryApp
#import sqlite3
from bd.conexion import Conexion

pacientes = []

color_fuente = 'black'

class MasterPanel:

    def __init__(self, tipousuario):
        self.indice_paciente = 0  # Mover la variable global aquí
        self.incremento = 10
        self.fuente_titulo = 'Comic Sans MS'
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        self.color_fuente1, self.color_fuente2 = utl.definir_color_fuente()
        self.color_fondo1, self.color_fondo2 = utl.definir_color_fondo()
        self.ventana= tk.Tk()
        self.ventana.title('DentalMatic')
        self.ventana.geometry('1000x500+200+80')
        self.ventana.config(bg= self.color_fondo2)
        self.ventana.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.ventana, 900, 600)
        self.menu = True
        self.imagen_ventana = utl.leer_imagen('tooth.jpg', (38, 38))
        self.ventana.iconphoto(False, self.imagen_ventana)
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)
        self.db = Conexion()
        self.miConexion = self.db.conectar()
        self.mes_estadistica = ''
        self.dni_paciente = StringVar()
        self.dato_paciente = StringVar()
        self.dato_paciente2 = StringVar()
        self.nombre_usuario = StringVar()
        self.matricula = StringVar()
        self.tipo_usuario = tipousuario

        self.frame_inicio = Frame(self.ventana, bg= self.color_fondo1, width= 50, height= 45)
        self.frame_inicio.grid_propagate(0)
        self.frame_inicio.grid(column= 0, row= 0, sticky= 'nsew')
        self.frame_menu = Frame(self.ventana, bg= self.color_fondo1, width= 60)
        self.frame_menu.grid_propagate(0)
        self.frame_menu.grid(column= 0, row= 1, sticky= 'nsew')
        self.frame_top = Frame(self.ventana, bg= self.color_fondo1, height= 50)
        self.frame_top.grid(column= 1, row= 0, sticky= 'nsew')
        self.frame_raiz = Frame(self.ventana, bg= self.color_fondo1)
        self.frame_raiz.grid(column= 1, row= 1, sticky= 'nsew')
        self.ventana.columnconfigure(1, weight= 1)
        self.ventana.rowconfigure(1, weight= 1)
        self.frame_raiz.columnconfigure(0, weight= 1)
        self.frame_raiz.rowconfigure(0, weight= 1)

        self.widgets()

    def menu_lateral(self):
        if self.menu is True:
            for i in range(50, 170, 10):
                self.frame_menu.config(width= i)
                self.frame_inicio.config(width= i)
                self.frame_menu.update()
                clik_inicio = self.bt_cerrar.grid_forget()
                if clik_inicio is None:
                    self.bt_inicio.grid(column= 0, row= 0, padx= 10, pady= 10)
                    self.bt_inicio.grid_propagate(0)
                    self.bt_inicio.config(width= i)
                    self.pantalla_inicial()
            self.menu = False
        else:
            for i in range(170, 50, -10):
                self.frame_menu.config(width=  i)
                self.frame_inicio.config(width= i)
                self.frame_menu.update()
                clik_inicio = self.bt_inicio.grid_forget()
                if clik_inicio is None:
                    self.frame_menu.grid_propagate(0)
                    self.bt_cerrar.grid(column= 0, row= 0, padx= 10, pady= 10)
                    self.bt_cerrar.grid_propagate(0)
                    self.bt_cerrar.config(width= i)
                    self.pantalla_inicial()
                self.menu = True

    def pantalla_inicial(self):
        self.paginas.select([self.frame_principal])

    def pantalla_usuarios(self):
        self.paginas.select([self.frame_usuarios])        
        [self.frame_tabla_usuario.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_usuarios.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_tabla_usuario.rowconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[1])]
        [self.frame_tabla_odontologos.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_usuarios.columnconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[0])]
        [self.frame_tabla_odontologos.rowconfigure(i, weight= 1) for i in range(self.frame_usuarios.grid_size()[1])]

    def pantalla_pacientes(self):
        self.paginas.select([self.frame_pacientes])
        [self.frame_tabla_paciente.columnconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_pacientes.columnconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[0])]
        [self.frame_tabla_paciente.rowconfigure(i, weight= 1) for i in range(self.frame_pacientes.grid_size()[1])]

    def pantalla_calendario(self):
        self.paginas.select([self.frame_calendario])
        cal = Calendario()
        cal.crear_encabezado(self.frame_calendario)
        cal.crear_botones_fechas(self.frame_calendario)
        cal.marcar_dia_turno()
        cal.actualizar_botones_fechas()
        cal.configurar_filas_columnas(self.frame_calendario)

    def pantalla_historia(self):
        self.paginas.select([self.frame_historia])
        [self.frame_tabla_historia.columnconfigure(i, weight= 1) for i in range(self.frame_historia.grid_size()[0])]
        [self.frame_historia.columnconfigure(i, weight= 1) for i in range(self.frame_historia.grid_size()[0])]
        [self.frame_tabla_historia.rowconfigure(i, weight= 1) for i in range(self.frame_historia.grid_size()[1])]

    def pantalla_herramientas(self):
        self.paginas.select([self.frame_herramientas])
        backup= Backup(master_panel=self)
        backup.configurar_interfaz(self.frame_herramientas)
        backup.listar_bases_datos()
        informes = Informes()
        informes.configurar_interfaz(self.frame_herramientas)
        pass

    def pantalla_galeria(self):
        self.paginas.select([self.frame_galeria])
        [self.frame_tabla_galeria.columnconfigure(i, weight= 1) for i in range(self.frame_galeria.grid_size()[0])]
        [self.frame_galeria.columnconfigure(i, weight= 1) for i in range(self.frame_galeria.grid_size()[0])]
        [self.frame_tabla_galeria.rowconfigure(i, weight= 1) for i in range(self.frame_galeria.grid_size()[1])]

    def salir(self):
        answer = messagebox.askokcancel('Salir', '¿Desea salir?', icon= 'warning', parent= self.ventana)
        if answer:
            #self.db.cerrar_bd()
            self.ventana.destroy()
            from modulos.modulo_login import Login
            Login()

    def agregar_paciente(self):
        paciente= Paciente()
        paciente.ventana_paciente(master_panel_ref=self)

    def editar_paciente(self, event):
        item = self.tabla_paciente.focus()
        if item:
            self.data = self.tabla_paciente.item(item)
            try:
                self.dni_paciente = self.data['values'][2]
                paciente = Paciente()
                paciente.cargar_datos(self.dni_paciente)
                paciente.ventana_paciente(master_panel_ref=self)
            except Exception as e:
                messagebox.showerror("ERROR", f"No se pudo cargar el paciente: {e}", parent= self.ventana)

    def editar_paciente2(self):
        item = self.tabla_paciente.focus()
        if item:
            self.data = self.tabla_paciente.item(item)
            try:
                self.dni_paciente = self.data['values'][2]
                paciente = Paciente()
                paciente.cargar_datos(self.dni_paciente)
                paciente.ventana_paciente(master_panel_ref=self)
            except Exception as e:
                messagebox.showerror("ERROR", f"No se pudo cargar el paciente: {e}", parent= self.ventana)
    
    def abrir_galeria(self, event):
        item = self.tabla_galeria.focus()
        if item:
            self.data = self.tabla_galeria.item(item)
            try:
                self.dni_paciente = self.data['values'][2]
                gal = Galeria()
                if gal.crear_carpeta(self.dni_paciente):
                    gal.cargar_paciente(self.dni_paciente)
                    gal.ventana_gal()
            except Exception as e:
                messagebox.showerror("ERROR", f"No se pudo cargar la galeria: {e}", parent= self.ventana)

    def editar_odontograma(self, event):
        item = self.tabla_historia.focus()
        if item:
            self.data = self.tabla_historia.item(item)
            try:
                self.dni_paciente = self.data['values'][2]
                odonto = Odontograma()
                odonto.cargar_paciente(self.dni_paciente)
                odonto.ventana_odonto()
            except Exception as e:
                messagebox.showerror("ERROR", f"No se pudo cargar el odontograma: {e}", parent= self.ventana)

    def eliminar_paciente(self):
        try:
            self.miCursor = self.miConexion.cursor()
            msg_box = messagebox.askquestion('Eliminar paciente', '¿Desea elminar al paciente?', icon='warning', parent= self.ventana)
            if msg_box == 'yes':
                self.miCursor.execute("DELETE FROM Pacientes WHERE ID = ?", (self.dni_paciente,))
                self.miConexion.commit()
                messagebox.showinfo("ELIMINAR","Paciente eliminado exitosamente")
                self.mostrar_pacientes()
                self.dni_paciente=[]
        except sqlite3.Error as e:
            messagebox.showerror("ERROR", f"No se pudo eliminar el paciente: {e}", parent= self.ventana)
        except Exception as e:
            messagebox.showerror("ERROR", f"Error inesperado: {e}", parent= self.ventana)

    def cargar_tabla_pacientes(self):
        #self.db.cerrar_bd()
        self.miConexion = self.db.conectar()
        """Carga todos los pacientes desde la base de datos."""
        try:
            cursor = self.miConexion.cursor()
            cursor.execute("SELECT Apellido, Nombre, ID, Telefono, ObraSocial FROM Pacientes ORDER BY Apellido")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {e}", parent= self.ventana)
            return []

    def cargar_pacientes_paginados(self):
        """Muestra los pacientes paginados de acuerdo al índice actual y controla los botones de navegación."""
        pacientes = self.cargar_tabla_pacientes()
        total = len(pacientes)
        inicio = self.indice_paciente
        fin = min(inicio + self.incremento, total) # Control de índice final

        # Limpiar la tabla antes de insertar nuevos datos
        self.tabla_paciente.delete(*self.tabla_paciente.get_children())

        # Insertar pacientes en la tabla
        for i in range(inicio, fin):
            self.tabla_paciente.insert('', 'end', text= pacientes[i][0], values= pacientes[i][1:])

        # --- Control de botones ---
        # Botón previo
        if self.indice_paciente == 0:
            self.boton_previo.config(state= 'disabled', bg= 'gray') # Desactivado y gris
        else:
            self.boton_previo.config(state= 'normal', bg= self.color_fondo1) # Activado y verde

        # Botón siguiente
        if fin >= total:
            self.boton_pos.config(state= 'disabled', bg= 'gray') # Desactivado y gris
        else:
            self.boton_pos.config(state= 'normal', bg= self.color_fondo1) # Activado y verde

    def cargar_pacientes_previos(self):
        """Carga la página anterior de pacientes."""
        self.indice_paciente = max(0, self.indice_paciente - self.incremento) # No permite índice negativo
        self.cargar_pacientes_paginados()

    def cargar_pacientes_posteriores(self):
        """Carga la página siguiente de pacientes."""
        pacientes = self.cargar_tabla_pacientes()
        total = len(pacientes)
        if self.indice_paciente + self.incremento < total:
            self.indice_paciente += self.incremento # Avanza a la siguiente página
        self.cargar_pacientes_paginados()

    def mostrar_pacientes(self):
        self.boton_pos.config(state= 'normal', bg= self.color_fondo1)
        self.boton_previo.config(state= 'disabled', bg= self.color_fondo1)
        self.indice_paciente= 0
        self.miConexion = self.db.conectar()
        self.miCursor = self.miConexion.cursor()
        bd = "SELECT Apellido, Nombre, ID, Telefono, ObraSocial FROM Pacientes ORDER BY Apellido"
        self.miCursor.execute(bd)
        datos = self.miCursor.fetchall()

        self.tabla_paciente.delete(*self.tabla_paciente.get_children())
        if (len(datos) > self.incremento):
            for i in range(0, self.incremento):
                    self.tabla_paciente.insert('', i, text= datos[i][0], values= datos[i][0:])
        else:
            self.boton_pos.config(state= 'disabled', bg= self.color_fondo1)
            for i in range(0, len(datos)):
                    self.tabla_paciente.insert('', i, text= datos[i][0], values= datos[i][0:])

    def buscar_paciente(self, event= None):
        """Busca pacientes por nombre o apellido y muestra mensaje si no hay resultados."""
        buscar = self.dato_paciente.get()
        try:
            cursor = self.miConexion.cursor()
            cursor.execute(
                "SELECT Apellido, Nombre, ID, Telefono, ObraSocial FROM Pacientes WHERE Apellido LIKE ? OR Nombre LIKE ? OR ID LIKE ? ORDER BY Apellido",
                (f'%{buscar}%', f'%{buscar}%', f'{buscar}%')
            )
            datos = cursor.fetchall()
            self.tabla_paciente.delete(*self.tabla_paciente.get_children())

            if datos:  # Si encuentra resultados
                for i, dato in enumerate(datos):
                    self.tabla_paciente.insert('', 'end', text= dato[0], values= dato[0:])
            else:  # Si no encuentra resultados
                messagebox.showinfo("BUSCAR", "No se encontraron coincidencias", parent= self.ventana)

        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar paciente: {e}", parent= self.ventana)

    def buscar_historia(self, event=None):
        """Busca historia clínica por apellido, nombre o DNI y muestra mensaje si no hay resultados."""
        buscar = self.dato_paciente2.get()
        try:
            cursor = self.miConexion.cursor()
            cursor.execute(
                "SELECT Apellido, Nombre, ID, ObraSocial FROM Pacientes WHERE Apellido LIKE ? OR Nombre LIKE ? OR ID LIKE ? ORDER BY Apellido",
                (f'%{buscar}%', f'%{buscar}%', f'{buscar}%')
            )
            datos = cursor.fetchall()

            # Limpiar tabla antes de insertar nuevos datos
            self.tabla_historia.delete(*self.tabla_historia.get_children())

            if datos:  # Si encuentra resultados
                for i, dato in enumerate(datos):
                    self.tabla_historia.insert('', 'end', values= dato)
            else:  # Si no encuentra resultados
                messagebox.showinfo("BUSCAR", "No se encontraron coincidencias", parent= self.ventana)

        except Exception as e:
            messagebox.showerror("ERROR", f"Error en la búsqueda: {e}", parent= self.ventana)

    def buscar_galeria(self, event=None):
        """Busca historia clínica por apellido, nombre o DNI y muestra mensaje si no hay resultados."""
        buscar = self.dato_paciente2.get()
        try:
            cursor = self.miConexion.cursor()
            cursor.execute(
                "SELECT Apellido, Nombre, ID, ObraSocial FROM Pacientes WHERE Apellido LIKE ? OR Nombre LIKE ? OR ID LIKE ? ORDER BY Apellido",
                (f'%{buscar}%', f'%{buscar}%', f'{buscar}%')
            )
            datos = cursor.fetchall()

            # Limpiar tabla antes de insertar nuevos datos
            self.tabla_galeria.delete(*self.tabla_galeria.get_children())

            if datos:  # Si encuentra resultados
                for i, dato in enumerate(datos):
                    self.tabla_galeria.insert('', 'end', values= dato)
            else:  # Si no encuentra resultados
                messagebox.showinfo("BUSCAR", "No se encontraron coincidencias", parent= self.ventana)

        except Exception as e:
            messagebox.showerror("ERROR", f"Error en la búsqueda: {e}", parent= self.ventana)

    def seleccionar_paciente(self, event):
        item = self.tabla_paciente.focus()
        self.data = self.tabla_paciente.item(item)
        try:
            self.dni_paciente = self.data['values'][2]
        except:
            pass

    def mostrar_usuarios(self):
        try:
            CONSULTA_USUARIOS = """
                SELECT nombre_usuario, pass_usuario, tipo_usuario 
                FROM usuarios where nombre_usuario NOT LIKE "admin"
                ORDER BY nombre_usuario
            """
            MASCARA_CONTRASENA = "********"

            cur = self.miConexion.cursor()
            cur.execute(CONSULTA_USUARIOS)
            datos = cur.fetchall()

            # Limpiar tabla existente
            self.tabla_usuario.delete(*self.tabla_usuario.get_children())

            # Insertar nuevos datos
            for nombre, _, tipo in datos:
                self.tabla_usuario.insert('', 'end', values= (nombre, MASCARA_CONTRASENA, tipo))

        except Exception as e:
            # Mostrar error al usuario
            messagebox.showerror(
                "Error al cargar usuarios",
                f"No se pudieron cargar los usuarios:\n{str(e)}\n\n"
                "Por favor verifique la conexión a la base de datos e intente nuevamente."
                , parent= self.ventana
            )

    def seleccionar_usuario(self, event):
        selected_item = self.tabla_usuario.selection()
        if selected_item:
            item = self.tabla_usuario.item(selected_item)
            self.nombre_usuario= item['values'][0]

    def agregar_usuario(self):
        user = Usuario()
        user.ventana(master_panel_ref=self)

    def editar_user(self):
        item = self.tabla_usuario.focus()
        if item:
            self.data = self.tabla_usuario.item(item)
            try:
                self.nombre_usuario = self.data['values'][0]
                user = Usuario()
                user.cargar_datos(self.nombre_usuario)
                user.ventana(master_panel_ref = self)
            except Exception as e:
                messagebox.showerror("ERROR", f"No se pudo cargar el usuario: {e}", parent= self.ventana)

    def editar_usuario(self, event):
        region = self.tabla_usuario.identify("region", event.x, event.y)
        if region == "heading":  # Si el doble clic es en el encabezado
            return
        else:
            try:
                selected_item = self.tabla_usuario.selection()
                item = self.tabla_usuario.item(selected_item)
                self.usuario= item['values'][0]
                if self.usuario != 'Usuario':
                    user = Usuario()
                    user.cargar_datos(self.usuario)
                    user.ventana(master_panel_ref=self)
                else:
                    messagebox.showwarning("Advertencia", "Debe seleccionar un usuario", parent= self.ventana)
            except:
                messagebox.showwarning("Advertencia", "Debe seleccionar un usuario", parent= self.ventana)

    def eliminar_usuario(self):
        try:
            user = Usuario()
            user.eliminar_usuario(self.nombre_usuario)
            self.mostrar_usuarios()
        except:
            messagebox.showwarning("Usuario", "No se pudo eliminar el usuario", parent= self.ventana)

    def mostrar_odontologos(self):
        try:
            CONSULTA_ODONTOLOGOS = """
                SELECT Matricula, Apellido_odontologo, Nombre_odontologo 
                FROM odontologos
                ORDER BY Apellido_odontologo
            """

            cur = self.miConexion.cursor()
            cur.execute(CONSULTA_ODONTOLOGOS)
            datos = cur.fetchall()

            # Limpiar tabla existente
            self.tabla_odontologos.delete(*self.tabla_odontologos.get_children())

            # Insertar nuevos datos
            for matricula, apellido_odontologo, nombre_odontologo in datos:
                self.tabla_odontologos.insert('', 'end', values= (apellido_odontologo, nombre_odontologo, matricula))

        except Exception as e:
            # Mostrar error al usuario
            messagebox.showerror(
                "Error al cargar odontologos",
                f"No se pudieron cargar los odontologos:\n{str(e)}\n\n"
                "Por favor verifique la conexión a la base de datos e intente nuevamente."
                , parent= self.ventana
            )

    def seleccionar_odontologo(self, event):
        selected_item = self.tabla_odontologos.selection()
        if selected_item:
            item = self.tabla_odontologos.item(selected_item)
            self.matricula= item['values'][2]

    def agregar_odontologo(self):
        profesional = Odontologo()
        profesional.ventana(master_panel_ref = self)

    def editar_odontologo(self, event):
        region = self.tabla_odontologos.identify("region", event.x, event.y)
        if region == "heading":  # Si el doble clic es en el encabezado
            return
        else:
            try:
                selected_item = self.tabla_odontologos.selection()
                item = self.tabla_odontologos.item(selected_item)
                matricula=item['values'][2]
                if matricula != '':
                    profesional = Odontologo()
                    profesional.cargar_datos(matricula)
                    profesional.ventana(master_panel_ref = self)
                else:
                    messagebox.showwarning("Advertencia", "Debe seleccionar un profesional", parent= self.ventana)
            except:
                messagebox.showwarning("Advertencia", "Debe seleccionar un profesional", parent= self.ventana)

    def editar_profesional(self):
        item = self.tabla_odontologos.focus()
        if item:
            self.data = self.tabla_odontologos.item(item)
            try:
                matricula = self.data['values'][2]
                profesional = Odontologo()
                profesional.cargar_datos(matricula)
                profesional.ventana(master_panel_ref = self)
            except:
                return
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un profesional", parent= self.ventana)

    def eliminar_odontologo(self):
        try:
            profesional = Odontologo()
            profesional.eliminar_odontologo(self.matricula)
            self.mostrar_odontologos()
        except:
            pass

    def abrir_ayuda_chm(self):
        # Obtener la ruta absoluta del archivo CHM
        base_dir = os.path.dirname(os.path.abspath(__file__))
        util_dir = os.path.join(os.path.dirname(base_dir), 'util')
        chm_path = os.path.join(util_dir, 'AyudaMyM.chm')
        
        if not os.path.exists(chm_path):
            messagebox.showerror("Error", 
                f"El archivo de ayuda no se encuentra en la ubicación esperada:\n{chm_path}")
            return

        try:
            if sys.platform == "win32":
                # Windows - método nativo
                os.startfile(chm_path)
                
            elif sys.platform == "darwin":
                # macOS - intentar con aplicaciones disponibles
                try:
                    subprocess.Popen(["open", chm_path])
                except:
                    # Alternativa para macOS
                    subprocess.Popen(["qlmanage", "-p", chm_path])
                    
            else:
                # Linux y otros sistemas
                try:
                    # Intentar con xdg-open (estándar en Linux)
                    subprocess.Popen(["xdg-open", chm_path])
                except FileNotFoundError:
                    # Alternativas para Linux
                    try:
                        subprocess.Popen(["kchmviewer", chm_path])
                    except FileNotFoundError:
                        try:
                            subprocess.Popen(["chmsee", chm_path])
                        except FileNotFoundError:
                            messagebox.showwarning(
                                "Advertencia", 
                                "No se encontró un visor CHM compatible. "
                                "Instale kchmviewer o chmsee."
                            )
                            return
                            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ayuda: {str(e)}")

        time.sleep(0.5)  # Pequeña pausa para evitar errores de apertura múltiple

    def widgets(self):
        self.imagen_usuario = utl.leer_imagen('usuario_icono.png', (38, 38))
        self.imagen_paciente = utl.leer_imagen('paciente.png', (38, 38))
        self.imagen_ayuda = utl.leer_imagen('ayuda.png', (20, 20))
        self.imagen_calendario = utl.leer_imagen('calendario.png', (38, 38))
        self.imagen_historia_clinica = utl.leer_imagen('odontograma.png', (38, 38))
        self.imagen_galeria = utl.leer_imagen('galeria.png', (38, 38))
        self.imagen_herramientas = utl.leer_imagen('statistics-removebg.png', (38, 38))
        self.imagen_agregar =  utl.leer_imagen('agregar.png', (30, 30))
        self.imagen_editar = utl.leer_imagen('editar.png', (38, 38))
        self.imagen_eliminar = utl.leer_imagen('eliminar.png', (30, 30))
        self.imagen_salir = utl.leer_imagen('salir.png', (38, 38))
        self.logo = utl.leer_imagen('logo1.png', (400, 400))

        try:
            self.imagen_inicio = utl.leer_imagen('home.png', (35, 35))
            self.imagen_menu = utl.leer_imagen('menu4.png', (38, 38))
            self.bt_inicio = Button(self.frame_inicio, image= self.imagen_inicio, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, image= self.imagen_menu, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.menu_lateral)
        except:
            self.bt_inicio = Button(self.frame_inicio, text= 'INICIO', font= (self.fuente_titulo, 12, 'bold'), bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.menu_lateral)
            self.bt_cerrar = Button(self.frame_inicio, text= '☰', font= ('Comic Sans MS', 12, 'bold'), bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.menu_lateral)

        self.bt_inicio.grid(column= 0, row= 0, padx= 5, pady= 10)
        self.bt_cerrar.grid(column= 0, row= 0, padx= 5, pady= 10)

        #BOTONES Y ETIQUETAS DEL MENU LATERAL
        Button(self.frame_menu, image= self.imagen_paciente, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.pantalla_pacientes).grid(column= 0, row= 2, pady= 20, padx= 10)
        Label(self.frame_menu, text= 'Pacientes', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 2, pady= 20, padx= 2)
        Button(self.frame_menu, image= self.imagen_calendario, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.pantalla_calendario ).grid(column= 0, row= 3, pady= 20, padx= 10)
        Label(self.frame_menu, text= 'Calendario', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 3, pady= 20, padx= 2)
        Button(self.frame_menu, image= self.imagen_salir, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.salir).grid(column= 0, row= 8, pady= 20, padx= 10)
        Label(self.frame_menu, text= 'Salir', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 8, pady= 20, padx= 2)

        if self.tipo_usuario == 'administrador' or self.tipo_usuario == 'odontologo':
            Button(self.frame_menu, image= self.imagen_historia_clinica, bg= self.color_fondo1,activebackground= 'white', bd= 0, command= self.pantalla_historia).grid(column= 0, row= 4, pady= 20, padx= 10)
            Label(self.frame_menu, text= 'Odontograma', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 4, pady= 20, padx= 2)
            Button(self.frame_menu, image= self.imagen_herramientas, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.pantalla_herramientas).grid(column= 0, row= 7, pady= 20, padx= 10)
            Label(self.frame_menu, text= 'Herramientas', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 7, pady= 20, padx= 2)
            Button(self.frame_menu, image= self.imagen_galeria, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.pantalla_galeria).grid(column= 0, row= 5, pady= 20, padx= 10)
            Label(self.frame_menu, text= 'Galeria', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 5, pady= 20, padx= 2)            

        if self.tipo_usuario == 'administrador':
            Button(self.frame_menu, image= self.imagen_usuario, bg= self.color_fondo1, activebackground= 'white', bd= 0, command= self.pantalla_usuarios).grid(column= 0, row= 1, pady= 20, padx= 10)
            Label(self.frame_menu, text= 'Usuarios', bg= self.color_fondo1, fg= 'white', font= (self.fuente_titulo, 10, 'bold')).grid(column= 1, row= 1, pady= 20, padx= 2)            

		#############################  CREAR  PAGINAS  ##############################
        self.estilo_paginas = ttk.Style(self.frame_raiz)
        self.estilo_paginas.layout('TNotebook.Tab', []) #desactiva las pestañas

        self.paginas = ttk.Notebook(self.frame_raiz, style= 'TNotebook')

        self.paginas.grid(column= 0, row= 0, sticky= 'nsew')
        self.frame_principal = Frame(self.paginas, bg= self.color_fondo2) #color de fondo
        self.frame_usuarios = Frame(self.paginas, bg= self.color_fondo2) #color de fondo
        self.frame_pacientes = Frame(self.paginas, bg= self.color_fondo2) #color de fondo
        self.frame_calendario = Frame(self.paginas, bg= self.color_fondo2)
        self.frame_historia = Frame(self.paginas, bg= self.color_fondo2)
        self.frame_herramientas = Frame(self.paginas, bg= self.color_fondo2)
        self.frame_galeria = Frame(self.paginas, bg= self.color_fondo2)
        self.paginas.add(self.frame_principal)
        self.paginas.add(self.frame_usuarios)
        self.paginas.add(self.frame_pacientes)
        self.paginas.add(self.frame_calendario)
        self.paginas.add(self.frame_historia)
        self.paginas.add(self.frame_galeria)
        self.paginas.add(self.frame_herramientas)

		##############################         PAGINAS       #############################################
		######################## FRAME TITULO #################
        self.frame_top.grid_columnconfigure(0, weight=1)  # Columna 0 se expande
        self.frame_top.grid_columnconfigure(1, weight=0)  # Columna 1 no se expande
        self.titulo = Label(self.frame_top, text= 'Consultorio Odontológico MyM', bg= self.color_fondo1, fg= 'white', font= ('Comic Sans MS', 15, 'bold'))
        self.titulo.grid(column= 0, row= 0, sticky='ew')
        self.boton_ayuda= Button(self.frame_top, image= self.imagen_ayuda, text= 'Ayuda', fg= 'black', font= self.fuenteb, bg= self.color_fondo1, command= self.abrir_ayuda_chm, relief= 'flat', borderwidth= 0, highlightthickness= 0, cursor= 'hand2', activebackground= self.color_fondo1)
        self.boton_ayuda.grid(column= 1, row= 0, sticky= 'e', padx= 10, pady= 10)
		######################## VENTANA PRINCIPAL #################
        Label(self.frame_principal, image= self.logo, bg= self.color_fondo2).pack(expand= 1)

        #ESTILO DE LAS TABLAS DE DATOS TREEVIEW
        self.estilo_tabla = ttk.Style(self.frame_usuarios)
        self.estilo_tabla.theme_use('alt')
        self.estilo_tabla.configure('TablaUsuario.Treeview', font= self.fuenten, foreground= 'black', rowheight= 20)
        self.estilo_tabla.map('Treeview.Heading', background= [("active", self.color_fondo1)], foreground= [("active", "white")])
        self.estilo_tabla.configure('TablaUsuario.Treeview.Heading', background= self.color_fondo1, foreground= 'white', padding= 3, font= self.fuenteb)
        self.estilo_paginas.layout('TNotebook.Tab', [])

        ######################## USUARIOS #################
        Label(self.frame_usuarios, text= 'USUARIOS', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 0, columnspan= 3, padx= 5, sticky="W")       
        Button(self.frame_usuarios, image= self.imagen_agregar, text= 'AGREGAR', fg= 'black', font= self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.agregar_usuario).grid(column= 0, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Agregar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 2)
        Button(self.frame_usuarios, image= self.imagen_eliminar, text= 'ELIMINAR', fg= 'black', font= self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.eliminar_usuario).grid(column= 1, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Eliminar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 1, row= 2)
        Button(self.frame_usuarios, image= self.imagen_editar, text= 'Editar', fg= 'black', font = self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.editar_user).grid(column= 2, row= 1, pady= 5)
        Label(self.frame_usuarios, text= 'Editar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 2, row= 2)

        #TABLA USUARIO
        self.frame_tabla_usuario = Frame(self.frame_usuarios, bg= self.color_fondo2)
        self.frame_tabla_usuario.grid(columnspan= 3, row= 3, sticky= 'nsew')
        self.tabla_usuario = ttk.Treeview(self.frame_tabla_usuario, columns= ("Usuario", "Clave", 'Tipo_usuario'), show= "headings", selectmode= 'browse', height= 6, style= "TablaUsuario.Treeview")
        self.tabla_usuario.grid(column= 0, row= 3, columnspan= 3, sticky='nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_usuario, orient= 'vertical', command= self.tabla_usuario.yview)
        ladoy.grid(column= 4, row= 3, sticky= 'ns')
        self.tabla_usuario.configure(yscrollcommand = ladoy.set)

        self.tabla_usuario.heading('Usuario', text= 'Usuario', anchor= 'center', command= lambda: None)
        self.tabla_usuario.heading('Clave', text= 'Clave', anchor= 'center', command= lambda: None)
        self.tabla_usuario.heading('Tipo_usuario', text= 'Tipo de usuario', anchor= 'center', command= lambda: None)
        self.mostrar_usuarios()
        self.tabla_usuario.bind("<Double-1>", self.editar_usuario)
        self.tabla_usuario.bind("<<TreeviewSelect>>", self.seleccionar_usuario)

        ######################## ODONTÓLOGOS #################
        Label(self.frame_usuarios, text= 'ODONTÓLOGOS', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 4, columnspan= 3, padx= 5, sticky= "W")       
        Button(self.frame_usuarios, image= self.imagen_agregar, text= 'AGREGAR', fg= 'black', font= self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.agregar_odontologo).grid(column= 0, row= 5, pady= 5)
        Label(self.frame_usuarios, text= 'Agregar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 6)
        Button(self.frame_usuarios, image= self.imagen_eliminar, text= 'ELIMINAR', fg= 'black', font= self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.eliminar_odontologo).grid(column= 1, row= 5, pady= 5)
        Label(self.frame_usuarios, text= 'Eliminar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 1, row= 6)
        Button(self.frame_usuarios, image= self.imagen_editar, text= 'Editar', fg= 'black', font = self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.editar_profesional).grid(column= 2, row= 5, pady= 5)
        Label(self.frame_usuarios, text= 'Editar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 2, row= 6)

        #TABLA ODONTÓLOGOS
        self.frame_tabla_odontologos = Frame(self.frame_usuarios, bg= self.color_fondo2)
        self.frame_tabla_odontologos.grid(columnspan= 3, row= 7, sticky= 'nsew')
        self.tabla_odontologos = ttk.Treeview(self.frame_tabla_odontologos, columns= ("Apellido", "Nombre", 'Matricula'), show= "headings", selectmode = 'browse', height= 6, style= "TablaUsuario.Treeview")
        self.tabla_odontologos.grid(column= 0, row= 7, columnspan= 3, sticky= 'nsew')
        ladoyy = ttk.Scrollbar(self.frame_tabla_odontologos, orient= 'vertical', command = self.tabla_odontologos.yview)
        ladoyy.grid(column = 4, row = 7, sticky= 'ns')
        self.tabla_odontologos.configure(yscrollcommand = ladoyy.set)
        self.tabla_odontologos.heading('Apellido', text= 'Apellido', anchor= 'center', command= lambda: None)
        self.tabla_odontologos.heading('Nombre', text= 'Nombre', anchor= 'center', command= lambda: None)
        self.tabla_odontologos.heading('Matricula', text= 'Matricula', anchor= 'center', command= lambda: None)
        self.mostrar_odontologos()
        self.tabla_odontologos.bind("<Double-1>", self.editar_odontologo)
        self.tabla_odontologos.bind("<<TreeviewSelect>>", self.seleccionar_odontologo)

		######################## PACIENTES #################
        Label(self.frame_pacientes, text= 'PACIENTES', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 0, columnspan= 4, padx= 5, sticky= "W")       
        Button(self.frame_pacientes, image= self.imagen_agregar, text= 'AGREGAR', fg= 'black', font= self.fuenten, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.agregar_paciente).grid(column= 0, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Agregar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 0, row= 2)
        Button(self.frame_pacientes, image= self.imagen_eliminar, text= 'ELIMINAR', fg= 'black', font= self.fuenten, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.eliminar_paciente).grid(column= 1, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Eliminar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 1, row= 2)
        Button(self.frame_pacientes, image= self.imagen_editar, text= 'Editar', fg= 'black', font = self.fuenten, bg= self.color_fondo1, bd= 2, borderwidth= 2, command= self.editar_paciente2).grid(column= 2, row= 1, pady= 5)
        Label(self.frame_pacientes, text= 'Editar', bg= self.color_fondo2, fg= 'black', font= self.fuenteb).grid(column= 2, row= 2)
        self.busqueda = ttk.Entry(self.frame_pacientes, textvariable= self.dato_paciente, width= 20, font= self.fuenten)
        self.busqueda.grid(column= 3, row= 1, pady= 5)
        Button(self.frame_pacientes, text= 'Buscar', bg= self.color_fondo1, fg= 'white', font= self.fuenteb, command= self.buscar_paciente).grid(column= 3, row= 2, pady= (0, 5))
        self.busqueda.bind('<Return>', (lambda event: self.buscar_paciente()))#es para apretar Intro y se ejecute, una opción a el botón

        self.boton_previo = tk.Button(self.frame_pacientes, text= '◀', fg= 'white', font = self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, width= 5, command= self.cargar_pacientes_previos)
        self.boton_previo.grid(column= 0, row= 3, padx= 10, pady=(0, 5), sticky= "W")
        self.boton_pos = tk.Button(self.frame_pacientes, text= '▶', fg= 'white', font = self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, width= 5, command= self.cargar_pacientes_posteriores)
        self.boton_pos.grid(column= 3, row= 3, padx= (0, 10), pady= (0, 5), sticky= "E")

		#TABLA PACIENTE
        self.frame_tabla_paciente = Frame(self.frame_pacientes, bg= self.color_fondo2)
        self.frame_tabla_paciente.grid(columnspan= 4, row= 4, sticky= 'nsew')
        self.tabla_paciente = ttk.Treeview(self.frame_tabla_paciente, columns= ('Apellido', 'Nombre', 'D.N.I.', 'Teléfono', 'Obra Social'), show= "headings", height= 16, selectmode= 'browse', style= "TablaUsuario.Treeview")
        self.tabla_paciente.grid(column= 0, row= 4, columnspan= 5, sticky= 'nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_paciente, orient= 'vertical', command= self.tabla_paciente.yview)
        ladoy.grid(column = 5, row = 4, sticky= 'ns')
        self.tabla_paciente.configure(yscrollcommand = ladoy.set)
        self.tabla_paciente.column('Apellido', minwidth= 100, width= 130 , anchor= 'w')
        self.tabla_paciente.column('Nombre', minwidth= 100, width= 130 , anchor= 'w')
        self.tabla_paciente.column('D.N.I.', minwidth= 100, width= 120, anchor= 'center')
        self.tabla_paciente.column('Teléfono', minwidth= 100, width= 120 , anchor= 'center')
        self.tabla_paciente.column('Obra Social', minwidth= 100, width= 105, anchor= 'center')

        self.tabla_paciente.heading('Apellido', text= 'Apellido', anchor= 'center')
        self.tabla_paciente.heading('Nombre', text= 'Nombre', anchor= 'center')
        self.tabla_paciente.heading('D.N.I.', text= 'D.N.I.', anchor = 'center')
        self.tabla_paciente.heading('Teléfono', text= 'Teléfono', anchor= 'center')
        self.tabla_paciente.heading('Obra Social', text= 'Obra Social', anchor= 'center')
        self.mostrar_pacientes()
        self.tabla_paciente.bind("<<TreeviewSelect>>", self.seleccionar_paciente)
        self.tabla_paciente.bind("<Double-1>", self.editar_paciente)

		######################## Odontograma #################
        Label(self.frame_historia, text= 'ODONTOGRAMA', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(columnspan= 4, row= 0, sticky= 'W')
        #Button(self.frame_historia, text= 'Nuevo odontograma', bg= self.color_fondo1, fg= 'white', font= self.fuenteb, command= self.editar_nuevo_odontograma).grid(column= 0, row= 1, padx=(10,5), pady= 5)
        self.busqueda2 = ttk.Entry(self.frame_historia, textvariable= self.dato_paciente2, width= 20, font= self.fuenten)
        self.busqueda2.grid(column= 2, row= 1, pady= 5, sticky= "e")
        self.busqueda3 = Button(self.frame_historia, text= 'Buscar', bg= self.color_fondo1, fg= 'white', font= self.fuenteb, command= self.buscar_historia)
        self.busqueda3.grid(column= 3, row= 1, padx= (10, 5), pady= 5)
        self.busqueda2.bind('<Return>', (lambda event: self.buscar_historia()))#es para apretar Intro y se ejecute, una opción a el botón

        self.frame_tabla_historia= Frame(self.frame_historia, bg= self.color_fondo2)
        self.frame_tabla_historia.grid(columnspan= 4, row= 4, sticky= 'nsew')
        self.tabla_historia = ttk.Treeview(self.frame_tabla_historia, columns= ("Apellido", "Nombre", "D.N.I.", "ObraSocial"), show= 'headings', height= 18, selectmode= 'browse', style= "TablaUsuario.Treeview")
        self.tabla_historia.grid(column= 0, row= 4, columnspan= 4, sticky= 'nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_historia, orient= 'vertical', command= self.tabla_historia.yview)
        ladoy.grid(column= 5, row= 4, sticky= 'ns')
        self.tabla_historia.configure(yscrollcommand = ladoy.set)

        self.tabla_historia.column('Apellido', minwidth= 100, width= 130 , anchor= 'w')
        self.tabla_historia.column('Nombre', minwidth= 100, width= 130 , anchor= 'w')
        self.tabla_historia.column('D.N.I.', minwidth= 100, width= 120, anchor= 'center')
        self.tabla_historia.column('ObraSocial', minwidth= 100, width= 105, anchor= 'center')

        self.tabla_historia.heading("Apellido", text= "Apellido")
        self.tabla_historia.heading("Nombre", text= "Nombre")
        self.tabla_historia.heading("D.N.I.", text= "D.N.I.")
        self.tabla_historia.heading("ObraSocial", text= "Obra social")

        self.tabla_historia.bind("<ButtonRelease-1>", self.editar_odontograma)

		######################## GALERIA #################
        Label(self.frame_galeria, text= 'GALERIA', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(column= 0, row= 0, sticky= 'W')
        self.busqueda_galeria_entry = ttk.Entry(self.frame_galeria, textvariable= self.dato_paciente2, width= 20, font= self.fuenten)
        self.busqueda_galeria_entry.grid(column= 2, row= 1, pady= 5, sticky="e")
        self.busqueda_galeria_entry.bind('<Return>', (lambda event: self.buscar_galeria()))#es para apretar Intro y se ejecute, una opción a el botón
        self.busqueda_galeria_boton = Button(self.frame_galeria, text= 'Buscar', bg= self.color_fondo1, fg= 'white', font= self.fuenteb, command= self.buscar_galeria)
        self.busqueda_galeria_boton.grid(column= 3, row= 1, padx= (10, 5), pady= 5)

        self.frame_tabla_galeria= Frame(self.frame_galeria, bg= self.color_fondo2)
        self.frame_tabla_galeria.grid(columnspan= 4, row= 4, sticky= 'nsew')
        self.tabla_galeria = ttk.Treeview(self.frame_tabla_galeria, columns= ("Apellido", "Nombre", "D.N.I.", "Obra social"), show= 'headings', height= 20, selectmode= 'browse', style= "TablaUsuario.Treeview")
        self.tabla_galeria.grid(column= 0, row= 4, columnspan= 4, sticky= 'nsew')
        ladoy = ttk.Scrollbar(self.frame_tabla_galeria, orient= 'vertical', command= self.tabla_galeria.yview)
        ladoy.grid(column = 4, row = 4, sticky= 'ns')
        self.tabla_galeria.configure(yscrollcommand = ladoy.set)
        self.tabla_galeria.heading("Apellido", text= "Apellido")
        self.tabla_galeria.heading("Nombre", text= "Nombre")
        self.tabla_galeria.heading("D.N.I.", text= "D.N.I.")
        self.tabla_galeria.heading("Obra social", text= "Obra social")

        self.tabla_galeria.bind("<ButtonRelease-1>", self.abrir_galeria)

        ######################## herramientas #################
        Label(self.frame_herramientas, text= 'HERRAMIENTAS', bg= self.color_fondo2, fg= self.color_fondo1, font= ('Comic Sans MS', 15, 'bold')).grid(columnspan= 3, row= 0, sticky= 'W')

        Label(self.frame_herramientas, text= 'Copia de seguridad (Backup)', bg= self.color_fondo2, font= self.fuenteb, relief= "groove", width= 125).grid(column= 0, row= 1, padx= (10, 0), pady= (0, 5), sticky= 'W')

        Label(self.frame_herramientas, text= 'Informes', bg= self.color_fondo2, font= self.fuenteb, relief= "groove", width= 125).grid(column= 0, row= 4, padx= (10, 0), pady= (0, 5), sticky= 'W')

        self.ventana.mainloop()