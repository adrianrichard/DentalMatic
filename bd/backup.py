import sqlite3
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import util.config as utl
from bd.conexion import Conexion

class Backup:
    def __init__(self, master_panel=None):  # Agregar parámetro master_panel
        super().__init__()
        self.bd_seleccionada = ''
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        self.color_fondo1, self.color_fondo2 = utl.definir_color_fondo()
        self.master_panel = master_panel  # Guardar referencia a la ventana principal

    def configurar_interfaz(self, frame):
        # Estilo de la tabla
        self.estilo_tablab = ttk.Style(frame)
        self.estilo_tablab.theme_use('alt')
        self.estilo_tablab.configure('TablaBackup.Treeview', font=self.fuenten, foreground='black', rowheight=20)
        self.estilo_tablab.configure('TablaBackup.Treeview.Heading', background=self.color_fondo1, foreground='white', padding=3, font=self.fuenteb)

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(frame, columns=("Nombre", "Fecha"), show="headings", height=8, style="TablaBackup.Treeview")
        self.tabla.heading("Nombre", text="Nombre BD")
        self.tabla.heading("Fecha", text="Fecha de creación")
        self.tabla.column('Nombre', width=350, anchor='w')
        self.tabla.column('Fecha', width=200, anchor='w')
        
        # Configurar grid
        self.tabla.grid(column=0, row=2, columnspan=3, padx=(10, 0), sticky='nsew')
        ladoy = ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        ladoy.grid(column=3, row=2, sticky='ns')
        self.tabla.configure(yscrollcommand=ladoy.set)

        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)

        # Listar las bases de datos en la tabla
        self.listar_bases_datos()

        self.frame_botones = tk.Frame(frame, bg=self.color_fondo2)
        self.frame_botones.grid(column=0, row=3, columnspan=4, sticky='ew', pady=10)
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=1)
        self.frame_botones.grid_columnconfigure(2, weight=1)
        btn_cargar_copia = tk.Button(self.frame_botones, text="Cargar backup", fg='white', 
                                   font=self.fuenteb, bg=self.color_fondo1, bd=2, borderwidth=2, 
                                   command=self.cargar_backup)
        btn_cargar_copia.grid(column=0, row=0, padx=(10, 5), pady=(5, 5))

        btn_guardar_copia = tk.Button(self.frame_botones, text= "Crear backup", fg= 'white', 
                                    font= self.fuenteb, bg= self.color_fondo1, bd= 2, borderwidth= 2, 
                                    command= self.crear_backup)
        btn_guardar_copia.grid(column= 1, row= 0, padx= 5, pady= (5, 5))

        btn_eliminar_copia = tk.Button(self.frame_botones, text= "Eliminar backup", fg='white', 
                                     font= self.fuenteb, bg='#d9534f', bd= 2, borderwidth= 2,
                                     command= self.eliminar_backup)
        btn_eliminar_copia.grid(column= 2, row= 0, padx= 5, pady= (5, 5))

    def obtener_carpeta_script(self):
        """Obtiene la ruta del directorio donde se encuentra el script Backup"""
        return os.path.dirname(os.path.abspath(__file__))

    def eliminar_backup(self):
        """Elimina la copia de seguridad seleccionada"""
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una copia de seguridad primero")
            return

        # Prevenir eliminación de la base de datos principal
        if self.bd_seleccionada == "consultorioMyM.sqlite3":
            messagebox.showerror("Error", "No se puede eliminar la base de datos principal")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar permanentemente la copia de seguridad:\n\n"
            f"'{self.bd_seleccionada}'?\n\n"
            "¡Esta acción no se puede deshacer!"
        )

        if not respuesta:
            return

        carpeta_script = self.obtener_carpeta_script()
        ruta_backup = os.path.join(carpeta_script, self.bd_seleccionada)

        # Verificar que el archivo existe
        if not os.path.exists(ruta_backup):
            messagebox.showerror("Error", f"No se encuentra el archivo: {self.bd_seleccionada}")
            return

        try:
            # Eliminar el archivo
            os.remove(ruta_backup)
            messagebox.showinfo("Éxito", f"Copia de seguridad eliminada: {self.bd_seleccionada}")

            # Limpiar selección y actualizar lista
            self.bd_seleccionada = ''
            self.listar_bases_datos()

        except PermissionError:
            messagebox.showerror("Error", "Permiso denegado. El archivo puede estar en uso.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el archivo: {e}")

    def cargar_backup(self):
        """Carga/restaura una copia de seguridad seleccionada"""
        if not self.bd_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una copia de seguridad primero")
            return

        # Prevenir restauración de la base de datos principal sobre sí misma
        if self.bd_seleccionada == "consultorioMyM.sqlite3":
            messagebox.showwarning("Advertencia", "No puede restaurar la base de datos principal sobre sí misma")
            return

        # Confirmar la acción con el usuario
        respuesta = messagebox.askyesno(
            "Confirmar restauración",
            f"¿Está seguro de que desea restaurar la base de datos principal usando:\n\n"
            f"'{self.bd_seleccionada}'?\n\n"
            "ADVERTENCIA: Esta acción sobrescribirá la base de datos actual y no se puede deshacer.\n"
            "La aplicación se cerrará y deberá volver a iniciar sesión."
        )

        if not respuesta:
            return

        carpeta_script = self.obtener_carpeta_script()
        
        # Definir nombres de archivos
        bd_principal = "consultorioMyM.sqlite3"
        bd_backup = self.bd_seleccionada
        
        ruta_backup = os.path.join(carpeta_script, bd_backup)
        ruta_principal = os.path.join(carpeta_script, bd_principal)
        
        # Verificar que el backup existe
        if not os.path.exists(ruta_backup):
            messagebox.showerror("Error", f"No se encuentra el backup: {bd_backup}")
            return

        try:
            # CERRAR TODAS LAS CONEXIONES EXISTENTES DE MANERA SEGURA
            try:
                Conexion.cerrar_todas_conexiones()
            except Exception as e:
                 messagebox.showerror(f"Advertencia al cerrar conexiones: {e}")
            
            # Verificar integridad del backup antes de restaurar
            if not self.verificar_integridad_bd(ruta_backup):
                messagebox.showerror("Error", "El archivo de backup está corrupto o no es una base de datos válida")
                # Intentar reconectar antes de salir
                Conexion.reconectar_todas()
                return
            
            # Realizar la restauración
            shutil.copy(ruta_backup, ruta_principal)
            
            # Verificar que la restauración fue exitosa
            if self.verificar_integridad_bd(ruta_principal):
                messagebox.showinfo(
                    "Éxito", 
                    f"Backup restaurado exitosamente!\n\n"
                    f"Base de datos principal: {bd_principal}\n"
                    f"Backup utilizado: {bd_backup}\n"
                    "La aplicación se cerrará automáticamente.\n"
                    "Por favor, inicie sesión nuevamente."
                )
                
                # CERRAR LA VENTANA PRINCIPAL DESPUÉS DE UN BREVE RETRASO
                self.cerrar_aplicacion()
                
            else:                
                messagebox.showerror("Error", "La restauración falló. La base de datos podría estar corrupta.")
                # Intentar reconectar incluso si falla
                Conexion.reconectar_todas()
                
        except PermissionError:
            messagebox.showerror("Error", "Permiso denegado. Asegúrese de que la base de datos no esté en uso.")
            Conexion.reconectar_todas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el backup: {e}")
            Conexion.reconectar_todas()
        finally:
            # Intentar reconectar siempre, incluso si falla
            try:
                Conexion.reconectar_todas()
            except:
                pass

    def cerrar_aplicacion(self):
        """Cierra la aplicación completamente usando la referencia a master_panel"""
        if self.master_panel and hasattr(self.master_panel, 'ventana'):
            # Cerrar la ventana principal
            self.master_panel.salir()

            # Opcional: Forzar cierre completo del proceso
            import sys
            sys.exit(0)
        else:
            # Si no hay referencia a master_panel, mostrar mensaje para cerrar manualmente
            messagebox.showinfo(
                "Backup Completado", 
                "Backup restaurado exitosamente.\n\n"
                "Por favor, cierre manualmente la aplicación e inicie sesión nuevamente."
            )

    def verificar_integridad_bd(self, ruta_bd):
        """Verifica que un archivo SQLite3 sea válido y no esté corrupto"""
        try:
            if not os.path.exists(ruta_bd):
                return False

            # Intentar conectar y ejecutar una consulta simple
            conn = sqlite3.connect(ruta_bd)
            cursor = conn.cursor()

            # Verificar integridad con PRAGMA integrity_check
            cursor.execute("PRAGMA integrity_check")
            resultado = cursor.fetchone()

            # Verificar que existen tablas esenciales
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()

            conn.close()

            # Si integrity_check retorna 'ok', la BD está intacta
            return resultado and resultado[0] == 'ok' and len(tablas) > 0

        except sqlite3.Error:
            return False
        except Exception:
            return False

    def crear_backup(self):
        """Crea una copia de seguridad de la base de datos"""
        carpeta_script = self.obtener_carpeta_script()
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
        nombre = 'consultorioMyM'

        ruta_original = os.path.join(carpeta_script, nombre + ".sqlite3")
        base_nombre = f"{nombre}_{fecha_actual}.sqlite3"
        ruta_copia = os.path.join(carpeta_script, base_nombre)

        try:
            # Verificar que la base de datos original existe
            if not os.path.exists(ruta_original):
                messagebox.showerror("Error", "No se encuentra la base de datos principal")
                return

            # Verificar integridad antes de hacer backup
            if not self.verificar_integridad_bd(ruta_original):
                messagebox.showwarning("Advertencia", "La base de datos principal podría tener problemas de integridad")

            shutil.copy(ruta_original, ruta_copia)

            # Verificar que el backup se creó correctamente
            if os.path.exists(ruta_copia) and self.verificar_integridad_bd(ruta_copia):
                messagebox.showinfo("Éxito", f"Backup creado exitosamente: {base_nombre}")
                self.listar_bases_datos()
            else:
                messagebox.showerror("Error", "El backup se creó pero podría estar corrupto")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el backup: {e}")

    def listar_bases_datos(self):
        """Lista todas las bases de datos .sqlite3 excepto la principal consultorioMyM.sqlite3"""
        carpeta_origen = self.obtener_carpeta_script()

        # Obtener todos los archivos .sqlite3 excluyendo la BD principal
        bases_datos = [
            f for f in os.listdir(carpeta_origen) 
            if f.endswith(".sqlite3") and f != "consultorioMyM.sqlite3"
        ]

        # Limpiar la tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Insertar las bases de datos en la tabla
        for base_datos in bases_datos:
            ruta_archivo = os.path.join(carpeta_origen, base_datos)
            try:
                fecha_creacion = datetime.fromtimestamp(os.path.getctime(ruta_archivo)).strftime('%Y-%m-%d %H:%M:%S')
                nombre_sin_extension = os.path.splitext(base_datos)[0]
                self.tabla.insert("", "end", values=(nombre_sin_extension, fecha_creacion))
            except OSError:
                self.tabla.insert("", "end", values=(os.path.splitext(base_datos)[0], "Fecha no disponible"))

        if not bases_datos:
            # Mostrar mensaje en la tabla si no hay backups
            self.tabla.insert("", "end", values=("No hay copias de seguridad", ""))

    def seleccionar_desde_tabla(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item[0])
            seleccion = item['values'][0]
            # Evitar seleccionar el mensaje de "No hay copias de seguridad"
            if seleccion != "No hay copias de seguridad":
                self.bd_seleccionada = seleccion + '.sqlite3'
            else:
                self.bd_seleccionada = ''

    def verificar_y_actualizar_conexiones(self):
        """Verifica que las conexiones estén activas y las reconecta si es necesario"""
        try:
            # Crear una nueva conexión temporal para verificar
            conexion_temp = sqlite3.connect('./bd/consultorioMyM.sqlite3')
            cursor_temp = conexion_temp.cursor()

            # Consulta simple de verificación
            cursor_temp.execute("SELECT 1")
            resultado = cursor_temp.fetchone()

            cursor_temp.close()
            conexion_temp.close()

            if resultado and resultado[0] == 1:
                messagebox.showerror("Base de datos verificada correctamente")
                # Reconectar todas las instancias existentes
                Conexion.reconectar_todas()
                return True
            else:
                messagebox.showerror(" Problemas con la consulta de verificación")
                return False

        except sqlite3.Error as e:
            messagebox.showerror(f"Error de conexión SQLite: {e}")
            return False
        except Exception as e:
            messagebox.showerror(f"Error inesperado: {e}")
            return False