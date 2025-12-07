import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pandas as pd
import sqlite3
import sys

# --- 1. CONFIGURACIÓN DE DATOS Y EJERCICIOS ---

# Tablas de datos de ejemplo (DataFrames de Pandas)
# Los nombres de las tablas se usarán en las consultas SQL
df_products = pd.DataFrame({
    'product_id': [1, 2, 3, 4],
    'name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'price': [1200, 25, 75, 300],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics']
})

df_sales = pd.DataFrame({
    'sale_id': [101, 102, 103, 104, 105],
    'product_id': [1, 3, 2, 4, 1],
    'quantity': [2, 5, 10, 1, 3],
    # CORREGIDO: Aseguramos que la lista tenga 5 elementos separados
    'sale_date': ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05'] 
})

# Renombrar DataFrames para que coincidan con los nombres de tabla en SQL
TABLES = {
    'products': {
        'df': df_products,
        'description': "Contiene información sobre los artículos que se venden.",
        'columns': "product_id (clave), name (nombre del producto), price (precio unitario), category (categoría)."
    },
    'sales': {
        'df': df_sales,
        'description': "Registra las transacciones de venta.",
        'columns': "sale_id (clave), product_id (clave foránea a 'products'), quantity (cantidad vendida), sale_date (fecha de venta)."
    }
}

# Definición de los ejercicios
# Cada ejercicio tiene un 'prompt' (instrucción) y un 'correct_query' (solución para la validación).
EXERCISES = [
    {
        'prompt': "Ejercicio 1/3: Muestra el `name` y el `price` de todos los productos. Ordena por nombre alfabéticamente.",
        'correct_query': "SELECT name, price FROM products ORDER BY name ASC"
    },
    {
        'prompt': "Ejercicio 2/3: Calcula la suma total de ítems vendidos (`quantity`) para el producto con `product_id` 1. Nombra la columna resultante como `total_sold`.",
        'correct_query': "SELECT SUM(quantity) AS total_sold FROM sales WHERE product_id = 1"
    },
    {
        'prompt': "Ejercicio 3/3: Encuentra el nombre (`name`) de los productos que pertenecen a la categoría 'Electronics' y cuyo precio (`price`) es superior a 100.",
        'correct_query': "SELECT name FROM products WHERE category = 'Electronics' AND price > 100"
    }
]

# --- 2. CLASE PRINCIPAL DE LA APLICACIÓN ---

class SQLTesterApp:
    def __init__(self, master, tables, exercises):
        # Configuración inicial
        self.master = master
        master.title("Evaluador de Conocimientos SQL")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.tables = tables
        self.exercises = exercises
        self.current_exercise_index = 0

        # Inicializar la base de datos en memoria
        self.conn = sqlite3.connect(':memory:')
        self._load_tables_to_db()

        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Inter', 10, 'bold'), padding=8)
        self.style.configure('TLabel', font=('Inter', 10))
        self.style.configure('Prompt.TLabel', font=('Inter', 12, 'bold'), foreground='#336699')
        self.style.configure('Info.TLabel', font=('Inter', 10, 'italic'), foreground='#555555')
        
        # Configurar la grid principal
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        # Contenedor de paneles (Izquierda y Derecha)
        main_frame = ttk.Frame(master, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # --- UI: Panel Izquierdo (Input y Schema) ---
        input_frame = ttk.Frame(main_frame, relief="flat", padding="5")
        input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        input_frame.grid_rowconfigure(2, weight=1) # Fila de la query
        input_frame.grid_columnconfigure(0, weight=1)

        # 1. Panel de Información de Tablas (Nuevo)
        schema_frame = ttk.LabelFrame(input_frame, text="ESQUEMA DE LA BASE DE DATOS", padding="10")
        schema_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.schema_text = tk.StringVar()
        self.schema_label = ttk.Label(schema_frame, textvariable=self.schema_text, 
                                     justify=tk.LEFT, wraplength=350, style='Info.TLabel')
        self.schema_label.pack(fill='x')
        self._update_schema_display()


        # 2. Área de Entrada de Query
        ttk.Label(input_frame, text="Escribe tu Consulta SQL aquí:", font=('Inter', 11, 'bold')).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        self.query_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=('Consolas', 10))
        self.query_input.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # Botones
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="EJECUTAR CONSULTA", command=self.execute_query, style='TButton').grid(row=0, column=0, sticky="ew", padx=2, pady=5)
        ttk.Button(button_frame, text="COMPROBAR SOLUCIÓN", command=self.check_solution, style='TButton').grid(row=0, column=1, sticky="ew", padx=2, pady=5)
        
        self.message_label = ttk.Label(input_frame, text="", foreground='blue', font=('Inter', 10, 'italic'))
        self.message_label.grid(row=4, column=0, sticky="ew", pady=(5, 0))

        # --- UI: Panel Derecho (Output) ---
        output_frame = ttk.Frame(main_frame, relief="flat", padding="5")
        output_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(output_frame, text="Resultado de la Consulta:", font=('Inter', 11, 'bold')).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.tree = ttk.Treeview(output_frame, show='headings')
        self.tree.grid(row=1, column=0, sticky='nsew')

        # Scrollbar vertical para el Treeview
        vsb = ttk.Scrollbar(output_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)
        
        # --- UI: Recuadro Inferior (Prompt) ---
        prompt_frame = ttk.Frame(master, padding="10 5", relief="groove")
        prompt_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.prompt_label = ttk.Label(prompt_frame, text="", style='Prompt.TLabel', wraplength=700)
        self.prompt_label.pack(expand=True, fill='x')

        # Cargar el primer ejercicio
        self.load_exercise()

    # --- 3. FUNCIONES DE BASE DE DATOS Y LÓGICA ---

    def _update_schema_display(self):
        """Genera y muestra el texto del esquema de la base de datos."""
        schema_info = ""
        for name, data in self.tables.items():
            schema_info += f"Tabla: {name.upper()}\n"
            schema_info += f"  - Descripción: {data['description']}\n"
            schema_info += f"  - Columnas: {data['columns']}\n\n"
        self.schema_text.set(schema_info.strip())

    def _load_tables_to_db(self):
        """Carga los DataFrames de Pandas a la base de datos SQLite en memoria."""
        try:
            for table_name, data in self.tables.items():
                data['df'].to_sql(table_name, self.conn, if_exists='replace', index=False)
            print("Tablas cargadas exitosamente en la DB en memoria.")
        except Exception as e:
            messagebox.showerror("Error de Inicialización", f"No se pudieron cargar las tablas: {e}")
            sys.exit(1)

    def execute_query(self):
        """Ejecuta la consulta del usuario y muestra el resultado en el Treeview."""
        query = self.query_input.get("1.0", tk.END).strip()
        if not query:
            self.message_label.config(text="Por favor, introduce una consulta SQL.")
            self.clear_treeview()
            return
        
        try:
            # Ejecutar la consulta y obtener el DataFrame resultante
            result_df = pd.read_sql_query(query, self.conn)
            self.display_result(result_df)
            self.message_label.config(text="Consulta ejecutada. Revisa los resultados a la derecha.")
        except Exception as e:
            self.clear_treeview()
            self.message_label.config(text=f"ERROR SQL: {e}", foreground='red')

    def display_result(self, df):
        """Muestra un DataFrame en el widget Treeview."""
        self.clear_treeview()

        # Configurar columnas
        columns = list(df.columns)
        self.tree["columns"] = columns
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize(), anchor="center")
            # Ajustar el ancho de las columnas (ejemplo: 80-150 píxeles)
            self.tree.column(col, anchor="center", width=int(self.tree.winfo_width() / len(columns) * 0.9) if self.tree.winfo_width() > 0 and len(columns) > 0 else 100)

        # Insertar filas
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))
            
    def clear_treeview(self):
        """Limpia el contenido del Treeview."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = [] # También limpia las columnas

    def check_solution(self):
        """Compara el resultado del usuario con la solución esperada."""
        user_query = self.query_input.get("1.0", tk.END).strip()
        
        if not user_query:
            self.message_label.config(text="No hay consulta para validar.", foreground='orange')
            return

        current_exercise = self.exercises[self.current_exercise_index]
        correct_query = current_exercise['correct_query']

        try:
            # 1. Obtener el resultado esperado
            expected_df = pd.read_sql_query(correct_query, self.conn)
            
            # 2. Obtener el resultado del usuario
            user_df = pd.read_sql_query(user_query, self.conn)

            # 3. Normalizar DataFrames para una comparación estricta
            user_df.columns = [c.lower() for c in user_df.columns]
            expected_df.columns = [c.lower() for c in expected_df.columns]
            
            # Asegurarse de que el orden de las columnas sea el mismo (SQL no garantiza el orden)
            if len(user_df.columns) == len(expected_df.columns):
                 user_df = user_df[expected_df.columns]
            
            # Compara el contenido de los DataFrames
            pd.testing.assert_frame_equal(
                expected_df.reset_index(drop=True), # Resetear índices para que no influyan
                user_df.reset_index(drop=True),
                check_dtype=True, # Comprueba si los tipos de datos son iguales
                check_exact=False, # Permite pequeñas diferencias en floats
                check_column_order=True # Asegúrate de que el orden y nombre de las columnas es el mismo
            )

            # Si la comparación es exitosa (no lanza error)
            self.message_label.config(text="¡CORRECTO! Pasando al siguiente ejercicio...", foreground='green')
            self.master.after(1500, self.next_exercise) # Espera 1.5s antes de avanzar

        except AssertionError as e:
            # Los DataFrames son diferentes (estructura o contenido)
            self.message_label.config(text="INCORRECTO. El resultado no coincide con la solución esperada.", foreground='red')
            print(f"Detalle de la diferencia (debug): {e}")
        except Exception as e:
            # Error de sintaxis o de ejecución de la consulta
            self.message_label.config(text=f"ERROR SQL o de validación: {e}", foreground='red')

    def load_exercise(self):
        """Carga el ejercicio actual en la UI."""
        if self.current_exercise_index < len(self.exercises):
            exercise = self.exercises[self.current_exercise_index]
            self.prompt_label.config(text=exercise['prompt'])
            self.query_input.delete("1.0", tk.END)
            self.clear_treeview()
            self.message_label.config(text="Escribe tu consulta y compruébala.", foreground='blue')
        else:
            # Final de los ejercicios
            self.master.destroy()
            messagebox.showinfo("¡Felicidades!", "Has completado todos los ejercicios. La aplicación se cerrará.")

    def next_exercise(self):
        """Avanza al siguiente ejercicio."""
        self.current_exercise_index += 1
        self.load_exercise()
        
    def on_closing(self):
        """Cierra la conexión a la DB y la aplicación."""
        if self.conn:
            self.conn.close()
        self.master.destroy()

# --- 4. EJECUCIÓN DEL SCRIPT ---

if __name__ == "__main__":
    # La aplicación requiere pandas y sqlite3 (que viene con python)
    try:
        root = tk.Tk()
        app = SQLTesterApp(root, TABLES, EXERCISES)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Ocurrió un error inesperado al iniciar la aplicación: {e}")