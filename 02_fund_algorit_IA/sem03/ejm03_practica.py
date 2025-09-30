import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
from statistics import mode, median

class SistemaNotas:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Notas")
        self.ventana.geometry("900x600")
        self.crear_bd()
        self.crear_interfaz()
        
    def crear_bd(self):
        conn = sqlite3.connect('estudiantes.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id TEXT PRIMARY KEY,
                nombres TEXT,
                apellidos TEXT,
                n1 REAL, n2 REAL, n3 REAL, n4 REAL, n5 REAL, n6 REAL,
                media REAL, mediana REAL, moda TEXT, nota_max REAL, nota_min REAL
            )
        ''')
        conn.commit()
        conn.close()
        
    def crear_interfaz(self):
        # Frame de entrada
        frame_entrada = tk.Frame(self.ventana)
        frame_entrada.pack(pady=10)
        
        # Campos de entrada
        tk.Label(frame_entrada, text="ID:").grid(row=0, column=0, padx=5)
        self.entry_id = tk.Entry(frame_entrada)
        self.entry_id.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_entrada, text="Nombres:").grid(row=0, column=2, padx=5)
        self.entry_nombres = tk.Entry(frame_entrada)
        self.entry_nombres.grid(row=0, column=3, padx=5)
        
        tk.Label(frame_entrada, text="Apellidos:").grid(row=0, column=4, padx=5)
        self.entry_apellidos = tk.Entry(frame_entrada)
        self.entry_apellidos.grid(row=0, column=5, padx=5)
        
        # Notas
        frame_notas = tk.Frame(self.ventana)
        frame_notas.pack(pady=10)
        
        self.entries_notas = []
        for i in range(6):
            tk.Label(frame_notas, text=f"N{i+1}:").grid(row=0, column=i*2, padx=5)
            entry = tk.Entry(frame_notas, width=8)
            entry.grid(row=0, column=i*2+1, padx=5)
            self.entries_notas.append(entry)
            
        # Botón registrar
        tk.Button(self.ventana, text="Registrar Estudiante", 
                 command=self.registrar_estudiante).pack(pady=10)
        
        # Tabla
        self.tree = ttk.Treeview(self.ventana, columns=(
            "ID", "Nombres", "Apellidos", "N1", "N2", "N3", "N4", "N5", "N6",
            "Media", "Mediana", "Moda", "Nota_Max", "Nota_Min"), show="headings", height=15)
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=60)
            
        self.tree.pack(pady=10, fill="both", expand=True)
        
    def calcular_estadisticas(self, notas):
        media = np.mean(notas)
        mediana = median(notas)
        
        # Verificar si hay moda real
        from collections import Counter
        contador = Counter(notas)
        max_freq = max(contador.values())
        
        if max_freq == 1:  # Todos los valores aparecen solo una vez
            moda = "No moda"
        else:
            moda = mode(notas)
            
        nota_max = max(notas)
        nota_min = min(notas)
        return media, mediana, moda, nota_max, nota_min
        
    def registrar_estudiante(self):
        try:
            # Obtener datos
            id_est = self.entry_id.get()
            nombres = self.entry_nombres.get()
            apellidos = self.entry_apellidos.get()
            notas = [float(entry.get()) for entry in self.entries_notas]
            
            if not all([id_est, nombres, apellidos]) or len(notas) != 6:
                messagebox.showerror("Error", "Rellene todos los campos")
                return
                
            # Calcular estadísticas
            media, mediana, moda, nota_max, nota_min = self.calcular_estadisticas(notas)
            
            # Insertar en tabla visual
            moda_display = moda if isinstance(moda, str) else f"{moda:.2f}"
            self.tree.insert("", "end", values=(
                id_est, nombres, apellidos, *notas, 
                f"{media:.2f}", f"{mediana:.2f}", moda_display, 
                f"{nota_max:.2f}", f"{nota_min:.2f}"
            ))
            
            # Guardar en base de datos
            conn = sqlite3.connect('estudiantes.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO estudiantes VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id_est, nombres, apellidos, *notas, media, mediana, moda, nota_max, nota_min))
            conn.commit()
            conn.close()
            
            # Guardar en CSV
            with open('estudiantes.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([id_est, nombres, apellidos, *notas, media, mediana, moda, nota_max, nota_min])
            
            # Limpiar campos
            self.entry_id.delete(0, tk.END)
            self.entry_nombres.delete(0, tk.END)
            self.entry_apellidos.delete(0, tk.END)
            for entry in self.entries_notas:
                entry.delete(0, tk.END)
                
            messagebox.showinfo("Éxito", "Estudiante registrado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Las notas deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")
            
    def ejecutar(self):
        self.ventana.mainloop()

# Crear encabezado CSV si este no existe
try:
    with open('estudiantes.csv', 'x', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombres', 'Apellidos', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 
                        'Media', 'Mediana', 'Moda', 'Nota_Max', 'Nota_Min'])
except FileExistsError:
    pass

# Ejecutar aplicación
if __name__ == "__main__":
    app = SistemaNotas()
    app.ejecutar()