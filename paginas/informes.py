import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
#from PIL import Image
from io import BytesIO
# import shutil
# from datetime import datetime
from tkinter import ttk, messagebox
import os
import util.config as utl
from bd.conexion import Conexion
#canvas = None

class Informes:
    def __init__(self):
        super().__init__()
        self.informe_seleccionado = ''  # Variable para almacenar la base de datos seleccionada
        self.fuenteb = utl.definir_fuente_bold()
        self.fuenten = utl.definir_fuente()
        self.db= Conexion()
        self.miConexion= self.db.conectar()
        self.miCursor= self.miConexion.cursor()

    def configurar_interfaz(self, frame):
        self.frame= frame
        # Estilo de la tabla
        self.estilo_tablai = ttk.Style(self.frame)
        self.estilo_tablai.theme_use('alt')
        self.estilo_tablai.configure('TablaInforme.Treeview', font= self.fuenten, foreground= 'black', rowheight= 20)
        self.estilo_tablai.configure('TablaInforme.Treeview.Heading', background= '#1F704B', foreground= 'white', padding= 3, font= self.fuenteb)

        # Crear la tabla para mostrar las bases de datos
        self.tabla = ttk.Treeview(self.frame, columns=("Informe", "Descripcion"), show= "headings", height= 6, style= "TablaInforme.Treeview")
        self.tabla.heading("Informe", text= "Informe")
        self.tabla.heading("Descripcion", text= "Descripción")
        self.tabla.column('Informe', width= 200 , anchor= 'w')
        self.tabla.column('Descripcion',  width= 350 , anchor= 'w')
        [self.frame.columnconfigure(i, weight= 1) for i in range(self.frame.grid_size()[0]-1)]
        self.tabla.grid(column= 0, row= 5, columnspan= 2, padx= (10,0), sticky= 'nsew')
        ladoy = ttk.Scrollbar(frame, orient= 'vertical', command = self.tabla.yview)
        ladoy.grid(column= 3, row= 5, sticky='ns')
        self.listar_informes()
        # Bind para seleccionar la base de datos desde la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_desde_tabla)
        self.tabla.bind("<Double-1>", self.graficar_ventana)

        btn_crear_grafico = tk.Button(frame, text= "Crear gráfica", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.graficar_ventana)
        btn_crear_grafico.grid(column= 0, row= 6, padx= (10, 10), pady= (5, 5))

    def graficar_ventana(self, event= None):
        if not self.informe_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un informe primero", parent= self.frame)
            return
        self.nueva_ventana = tk.Toplevel(self.frame)
        self.nueva_ventana.title('Informes')
        self.nueva_ventana.resizable(width= 0, height= 0)
        utl.centrar_ventana(self.nueva_ventana, 520, 520)
        self.nueva_ventana.grab_set_global() # Obliga a las ventanas estar deshabilitadas y deshabilitar todos los eventos e interacciones con la ventana
        self.nueva_ventana.focus_set() # Mantiene el foco cuando se abre la ventana.
        titulo = tk.Label(self.nueva_ventana, text= self.informe_seleccionado, fg='white', bg='#1F704B', relief= "raised", bd= 2, font= ("Arial", 16), anchor='center')
        titulo.grid(column= 0, row= 0, columnspan= 3, pady= (5, 5), padx= (5, 5), sticky='ew')
        anios= self.obtener_anios()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        if self.informe_seleccionado != 'Rango etario pacientes':
            self.selector_mes= ttk.Combobox(self.nueva_ventana, state= "readonly", values= meses, width= 20, background= "white")
            self.selector_mes.grid(column= 0, row= 1, padx= (10, 10), pady= (0, 5))
            self.selector_mes.set(meses[0])
            self.selector_anio= ttk.Combobox(self.nueva_ventana, state= "readonly", values= anios, width= 20, background= "white")
            self.selector_anio.grid(column= 1, row= 1, padx= (10, 10), pady= (0, 5))
            if anios != []:
                self.selector_anio.set(anios[0])
            else:
                self.selector_anio.set("No hay datos")
                self.selector_anio.config(state= "disabled")
        if self.informe_seleccionado == 'Cantidad de turnos' or self.informe_seleccionado == 'Horario de turnos por año' or self.informe_seleccionado == 'Prestaciones':
            self.selector_mes.config(state= "disabled")

        # Frame para el gráfico en la nueva ventana
        self.frame_grafico = tk.Frame(self.nueva_ventana, background= 'white', relief= "raised", width= 500, height= 400)
        self.frame_grafico.grid(column= 0, row= 3, columnspan= 3, pady= (10, 10), padx= (10, 10))
        self.frame_grafico.grid_propagate(False)
        boton_graficar = tk.Button(self.nueva_ventana, text= "Graficar", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.crear_grafica)
        boton_graficar.grid(column= 0, row= 2)
        boton_pdf = tk.Button(self.nueva_ventana, text= "Crear PDF", fg= 'white', font = self.fuenteb, bg= '#1F704B', bd= 2, borderwidth= 2, command= self.create_pdf)
        boton_pdf.grid(column= 1, row= 2)
        boton_salir = tk.Button(self.nueva_ventana, text= "Salir", command= self.salir, fg= 'white', bg= "orange", width= 8, font = self.fuenteb, bd= 2, borderwidth= 2)
        boton_salir.grid(column= 2, row= 2)

    def salir(self):
        plt.close('all')
        self.nueva_ventana.destroy()

    def listar_informes(self):
        # Limpiar la tabla si ya tiene datos
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        self.tabla.insert("", "end", values=('Cantidad de turnos', 'Turnos dados por mes cada año'))
        self.tabla.insert("", "end", values=('Horario de turnos por mes', 'Horarios con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Horario de turnos por año', 'Horarios con más demanda por año'))
        self.tabla.insert("", "end", values=('Día de turnos', 'Días con más demanda por mes y año'))
        self.tabla.insert("", "end", values=('Prestaciones', 'Prestaciones más frecuentes por año'))
        self.tabla.insert("", "end", values=('Rango etario pacientes', 'Distribución por edad'))

    def seleccionar_desde_tabla(self, event):#
        selected_item = self.tabla.selection()
        if selected_item:
            item = self.tabla.item(selected_item)
            self.informe_seleccionado=item['values'][0]
    
    def create_bar_chart(self):
        datos=[]
        valoresx=[]
        valoresy=[]
        self.fig, ax = plt.subplots(figsize=(4, 4))
        if self.informe_seleccionado == 'Cantidad de turnos':
            titulo='Cantidad de turnos por mes en '+self.selector_anio.get()
            datos = self.obtener_datos_por_mes_anio()
            valoresx = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            valoresy = [fila[1] for fila in datos]
            if not valoresy :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color= 'gray')
                ax.set_title('NO HAY DATOS')
            else:
                ax.bar(valoresx, valoresy, color= 'skyblue')  # Gráfico de barras
                ax.set_title(titulo, fontsize= 8, fontweight= 'bold', pad= 10)
                plt.xticks(rotation= 90)
            ax.set_xlabel('Meses')
            ax.set_ylabel('Cantidad de turnos')

        if self.informe_seleccionado == 'Horario de turnos por mes':
            titulo='Turnos por horario en el mes de '+self.selector_mes.get()+'-'+self.selector_anio.get()
            datos = self.obtener_horario_mes()
            if len(datos) == 0 :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color= 'gray')
                ax.set_title('NO HAY DATOS')
            else:
                valoresy = [fila[1] for fila in datos]
                valoresx = [fila[0] for fila in datos]
                ax.bar(valoresx, valoresy, color= 'skyblue')  # Gráfico de barras
            ax.set_xlabel('Horario')
            ax.set_ylabel('Cantidad de turnos')
            ax.set_title(titulo, fontsize= 8, fontweight= 'bold', pad= 10)
            plt.xticks(rotation= 90)

        if self.informe_seleccionado == 'Horario de turnos por año':
            titulo= 'Turnos por horario en el año '+self.selector_anio.get()
            datos = self.obtener_horario_anio()
            if not datos :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color= 'gray')
                ax.set_title('NO HAY DATOS')
            else:
                valoresy = [fila[1] for fila in datos]
                valoresx = [fila[0] for fila in datos]
                ax.bar(valoresx, valoresy, color= 'skyblue')  # Gráfico de barras
                ax.set_title(titulo, fontsize= 8, fontweight= 'bold', pad= 10)
                plt.xticks(rotation= 90)
            ax.set_xlabel('Horario')
            ax.set_ylabel('Cantidad de turnos')

        if self.informe_seleccionado == 'Día de turnos':
            titulo= 'Día de turnos en '+self.selector_mes.get()+'-'+self.selector_anio.get()
            datos = self.contar_dias_semana()            
            if not datos :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color= 'gray')
                ax.set_title('NO HAY DATOS')
            else:
                valoresy = [fila[1] for fila in datos]
                valoresx = [fila[0] for fila in datos]
                ax.bar(valoresx, valoresy, color= 'skyblue')
                ax.set_title(titulo)
                plt.xticks(rotation= 45)
            ax.set_xlabel('Días de la semana')
            ax.set_ylabel('Cantidad de turnos')

        if self.informe_seleccionado == 'Prestaciones':
            titulo= 'Prestaciones-'+self.selector_anio.get()
            datos = self.obtener_prestaciones_anio()   
            if not datos :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color='gray')
                ax.set_title('NO HAY DATOS')
            else:
                valoresy = [fila[1] for fila in datos]
                valoresx = [fila[0] for fila in datos]
                valoresx [3]= 'TRATAMIENTO DE\nCONDUCTO'
                ax.bar(valoresx, valoresy, color= 'skyblue')
                ax.set_title(titulo)
                plt.xticks(rotation= 0, fontsize=6)
            ax.set_xlabel('Prestaciones')
            ax.set_ylabel('Cantidad')

        if self.informe_seleccionado == 'Rango etario pacientes':
            titulo = 'Distribución de pacientes por edad'
            datos = self.obtener_distribucion_etaria()
            if not datos :  # Verificar si datos está vacío
                ax.text(0.5, 0.5, 'No hay datos disponibles\npara este período', ha= 'center', va= 'center', fontsize= 10, color= 'gray')
                ax.set_title('NO HAY DATOS')
            else:
                valoresy = [fila[1] for fila in datos]
                valoresx = [fila[0] for fila in datos]
                ax.bar(valoresx, valoresy, color= 'skyblue')
                
            ax.set_xlabel('Rango etario')
            ax.set_ylabel('Cantidad de pacientes')
            ax.set_title(titulo)
            plt.xticks(rotation= 0)

        plt.tight_layout()

        # Crear el canvas de matplotlib en Tkinter y asignarlo al frame de la nueva ventana
        canvas = FigureCanvasTkAgg(self.fig, self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().grid(row= 0, column= 0, columnspan= 3)

        # Cerrar los recursos de la figura
        buffer = BytesIO()
        plt.savefig(buffer, format= 'png', dpi= 300, bbox_inches= 'tight')
        plt.close(self.fig)
        buffer.seek(0)
        return buffer

    def crear_grafica(self):
        # Limpiar el frame del gráfico primero
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        plt.clf()
        plt.close('all')
        self.create_bar_chart()
        
# Función para obtener los datos agrupados por mes y año
    def obtener_anios(self):
        anios_unicos= []
        try:
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            self.miCursor.execute("SELECT DISTINCT strftime('%Y', Fecha) AS Año FROM Turnos ORDER BY Año DESC")
            anios_unicos = self.miCursor.fetchall()
            # Convertir los resultados a una lista de años
            anios_unicos = [anio[0] for anio in anios_unicos]
        except Exception as e:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "f'Error al obtener datos: {e}'", parent= self.frame)
            self.nueva_ventana.grab_set()

        return anios_unicos

    def obtener_datos_por_mes_anio(self):
        datos=[]
        try:
            # Consulta para obtener todos los meses, incluso los que no tienen turnos
            self.miCursor.execute("""
                WITH meses AS (
                    SELECT '01' as mes UNION SELECT '02' UNION SELECT '03' UNION SELECT '04'
                    UNION SELECT '05' UNION SELECT '06' UNION SELECT '07' UNION SELECT '08'
                    UNION SELECT '09' UNION SELECT '10' UNION SELECT '11' UNION SELECT '12'
                )
                SELECT m.mes, COALESCE(COUNT(t.Fecha), 0) AS CantidadTurnos
                FROM meses m
                LEFT JOIN Turnos t ON m.mes = strftime('%m', t.Fecha) 
                    AND strftime('%Y', t.Fecha) = ?
                GROUP BY m.mes
                ORDER BY m.mes
            """, (self.selector_anio.get(),))

            datos = self.miCursor.fetchall()
            return datos

        except Exception as e:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "f'Error al obtener datos por mes: {e}'", parent= self.frame)
            self.nueva_ventana.grab_set()
            # Retornar array con 12 meses y 0 turnos en caso de error
            return [(str(i).zfill(2), 0) for i in range(1, 13)]

    def mes_a_numero(self, nombre_mes):
        meses = {
            "enero": '01',
            "febrero": '02',
            "marzo": '03',
            "abril": '04',
            "mayo": '05',
            "junio": '06',
            "julio": '07',
            "agosto": '08',
            "septiembre": '09',
            "octubre": '10',
            "noviembre": '11',
            "diciembre": '12'
        }
        return meses.get(nombre_mes.lower(), "Mes no válido")

    def obtener_horario_mes(self):
    # Conexión a la base de datos (ajusta la ruta si usas sqlite)
        datos=[]
        mes= self.mes_a_numero(self.selector_mes.get())
        try:
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            self.miCursor.execute(""" SELECT Hora, COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? AND strftime('%m', Fecha) = ? GROUP BY Hora ORDER BY Hora ASC""", (self.selector_anio.get(),mes,))
            datos = self.miCursor.fetchall()
            #self.miConexion.close()
        except:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "No se pudo cargar", parent= self.frame)
            self.nueva_ventana.grab_set()
        return datos

    def obtener_horario_anio(self):
        datos= []
        try:
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            self.miCursor.execute(""" SELECT Hora, COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? GROUP BY Hora ORDER BY Hora ASC""", (self.selector_anio.get(),))
            datos = self.miCursor.fetchall()
            #self.miConexion.close()
        except:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "No se pudo cargar", parent= self.frame)
            self.nueva_ventana.grab_set()
        return datos

    def obtener_prestaciones_anio(self):
        datos= []
        try:
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            self.miCursor.execute(""" SELECT DISTINCT Prestacion, COUNT(*) AS Cantidad_prestaciones FROM Turnos WHERE strftime('%Y', Fecha) = ? GROUP BY Prestacion""", (self.selector_anio.get(),))
            datos = self.miCursor.fetchall()
            #self.miConexion.close()
        except:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "No se pudo cargar", parent= self.frame)
            self.nueva_ventana.grab_set()
        return datos

    def get_image_size(self, image_path, max_width, max_height):
        image_reader = ImageReader(image_path)
        img_width, img_height = image_reader.getSize()
        aspect_ratio = img_width / img_height

        if img_width > max_width:
            img_width = max_width
            img_height = img_width / aspect_ratio

        if img_height > max_height:
            img_height = max_height
            img_width = img_height * aspect_ratio

        return img_width, img_height

    def contar_dias_semana(self):
        datos=[]
        try:
            # Consulta SQL para agrupar por mes y año (en formato YYYY-MM)
            mes= self.mes_a_numero(self.selector_mes.get())
            self.miCursor.execute("SELECT CASE strftime('%w', Fecha)  WHEN '0' THEN 'Domingo'\
                WHEN '1' THEN 'Lunes'\
                WHEN '2' THEN 'Martes'\
                WHEN '3' THEN 'Miércoles'\
                WHEN '4' THEN 'Jueves'\
                WHEN '5' THEN 'Viernes'\
                WHEN '6' THEN 'Sábado'\
                END,\
                COUNT(*) AS Cantidad_Turnos FROM Turnos WHERE strftime('%Y', Fecha) = ? and strftime('%m', Fecha)= ? GROUP BY strftime('%w', Fecha) ORDER BY strftime('%w', Fecha)""", (self.selector_anio.get(),mes,))
            datos = self.miCursor.fetchall()
        except Exception as e:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "f'Error al obtener datos: {e}'", parent= self.frame)
            self.nueva_ventana.grab_set()

        return datos

    def obtener_distribucion_etaria(self):
        datos=[]
        try:
            query = """
            SELECT
                CASE
                    WHEN edad BETWEEN 5 AND 15 THEN '5-15'
                    WHEN edad BETWEEN 16 AND 25 THEN '16-25'
                    WHEN edad BETWEEN 26 AND 35 THEN '26-35'
                    WHEN edad BETWEEN 36 AND 50 THEN '36-50'
                    WHEN edad BETWEEN 51 AND 100 THEN '51-100'
                    ELSE 'Fuera de rango'
                END AS rango_etario,
                COUNT(*) AS cantidad_pacientes
            FROM pacientes
            GROUP BY 
                CASE
                    WHEN edad BETWEEN 5 AND 15 THEN '5-15'
                    WHEN edad BETWEEN 16 AND 25 THEN '16-25'
                    WHEN edad BETWEEN 26 AND 35 THEN '26-35'
                    WHEN edad BETWEEN 36 AND 50 THEN '36-50'
                    WHEN edad BETWEEN 51 AND 100 THEN '51-100'
                    ELSE 'Fuera de rango'
                END
            ORDER BY 
                CASE
                    WHEN rango_etario = '5-15' THEN 1
                    WHEN rango_etario = '16-25' THEN 2
                    WHEN rango_etario = '26-35' THEN 3
                    WHEN rango_etario = '36-50' THEN 4
                    WHEN rango_etario = '51-100' THEN 5
                    ELSE 6
                END
            """

            self.miCursor.execute(query)
            datos = self.miCursor.fetchall()

            return datos

        except Exception as e:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", "f'Error al obtener datos: {e}'", parent= self.frame)
            self.nueva_ventana.grab_set()

    def create_pdf(self):
        try:
            carpeta_informes = os.path.join(os.path.expanduser("."), "informes")
            if not os.path.exists(carpeta_informes):
                os.makedirs(carpeta_informes)
            if self.informe_seleccionado == 'Cantidad de turnos':
                pdf_filename='CantidadTurnos'+self.selector_anio.get()+'.pdf'
            elif self.informe_seleccionado == 'Horario de turnos por mes':
                pdf_filename='HorarioTurnos'+self.selector_mes.get()+self.selector_anio.get()+'.pdf'
            elif self.informe_seleccionado == 'Horario de turnos por año':
                pdf_filename='HorarioTurnos'+self.selector_anio.get()+'.pdf'
            elif self.informe_seleccionado == 'Día de turnos':
                pdf_filename='Día de turnos'+self.selector_mes.get()+self.selector_anio.get()+'.pdf'
            elif self.informe_seleccionado == 'Prestaciones':
                pdf_filename='Prestaciones-'+self.selector_anio.get()+'.pdf'
            elif self.informe_seleccionado == 'Rango etario pacientes':
                pdf_filename='Rango etario pacientes.pdf'
            else:
                pdf_filename='informe_generico.pdf'

            # pdf_filename = "documento_con_graficas.pdf"
            file_path = os.path.join(carpeta_informes, pdf_filename)
            document = SimpleDocTemplate(file_path, pagesize= A4)

            # Obtener los estilos de muestra
            styles = getSampleStyleSheet()

            # Contenido del PDF
            content = []
            
            # Añadir una imagen externa y mantener la relación de aspecto
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            directorio_padre = os.path.dirname(directorio_actual)
            carpeta_imagenes = os.path.join(directorio_padre, "imagenes")
            image_path = os.path.join(carpeta_imagenes, "LOGO11.png")
            max_width = 20 * cm
            max_height = 10 * cm
            if os.path.exists(image_path):
                img_width, img_height =self.get_image_size(image_path, max_width, max_height)
                logo_image = Image(image_path, width=img_width, height=img_height)
                content.append(logo_image)
                content.append(Paragraph("<font size='30'>&nbsp;</font>", styles['Normal']))
            else:
                title = Paragraph("MyM Odontología", styles['Title'])
                content.append(title)
                content.append(Paragraph("<font size='30'>&nbsp;</font>", styles['Normal']))

            # Título
            title = Paragraph("Informe", styles['Title'])
            content.append(title)
            content.append(Spacer(1, 5))

            # Crear gráficos y añadirlos al PDF
            bar_chart_buffer = self.create_bar_chart()
        # Calcular dimensiones proporcionales
            bar_chart_buffer.seek(0)
            img_reader = ImageReader(bar_chart_buffer)
            img_width, img_height = img_reader.getSize()
            aspect_ratio = img_width / img_height

            # Usar 80% del ancho de página y altura proporcional
            page_width = A4[0]
            max_chart_width = page_width * 0.8
            chart_height = max_chart_width / aspect_ratio

            bar_chart_image = Image(bar_chart_buffer, width= max_chart_width, height= chart_height)
            content.append(bar_chart_image)

            # line_chart_buffer = create_line_chart()
            # line_chart_image = Image(line_chart_buffer, width=4*inch, height=3*inch)
            # # content.append(line_chart_image)

            # pie_chart_buffer = create_pie_chart()
            # pie_chart_image = Image(pie_chart_buffer, width=4*inch, height=3*inch)
            # content.append(pie_chart_image)

            # Construir el documento PDF
            document.build(content)

            # Abrir el PDF con el visor predeterminado del sistema
            os.startfile(file_path)  # Para Windows
        except Exception as e:
            self.nueva_ventana.grab_release()
            messagebox.showwarning("Error", f'Error al crear el informe: {e}', parent= self.nueva_ventana)
            self.nueva_ventana.grab_set()
