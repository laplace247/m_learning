import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calcular_media():
    try:
        valores=[]
        for child in tree.get_children():
            val=tree.item(child)["values"][0]
            valores.append(float(val))
        if len(valores) == 0:
            messagebox.showerror("Aviso", "No hay datos en la tabla")
            return
        #Calcular la media
        media=sum(valores)/len(valores)
        ibi_resultado.config(text=f"Media: {media:.2f}")
        messagebox.showinfo("Resultado", f"La media es: {media:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Asegurate de ingresar numeros válidos")

def agregar_numero():
    try:
        valor=float(entry_numero.get())
        tree.insert("", "end", values=(valor,))
        entry_numero.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Asegurate de ingresar un numero válido")
#Crear formulario
ventana=tk.Tk()
ventana.title("Calcular la Media")
ventana.geometry("400x300")

#Campo ingresar numero
tk.Label(ventana, text="Ingrese un número:").pack(pady=5)
entry_numero=tk.Entry(ventana)
entry_numero.pack(pady=5)

#Botones
frame_botones=tk.Frame(ventana)
frame_botones.pack(pady=5)
tk.Button(frame_botones, text="Agregar", 
          command=agregar_numero).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Calcular Media",
          command=calcular_media).grid(row=0, column=1, padx=5)

#Tabla y Treeview
tree=ttk.Treeview(ventana,columns="numero", show="headings", height=5)
tree.heading("numero", text="numero")
tree.pack(pady=10)

#Resultado
ibi_resultado=tk.Label(ventana, text="Media:", font=("Arial", 12, "bold"))
ibi_resultado.pack(pady=10)

ventana.mainloop()