import os
import yaml
import shutil #Trabajar con las imagenes y etiquetas
import random

RUTA_BASE=r"C:\Users\Estudiante\Downloads\sem05\data"
RUTA_DATASET=os.path.join(RUTA_BASE,"dataset")
CLASES=['verdes','fresco','cancro','puntos negros']
DIV_ENTRENAMIENTO=0.8 #80% Entrenamiento - 20% validación

#Creación de carpetas
for subset in['train','val']:
    for tipo in ['images','labels']:
        os.makedirs(os.path.join(RUTA_DATASET,subset,tipo),exist_ok=True)

print("Carpetas creadas correctamente..")

#Dividir automaticamente las imagenes
for clase_id, clase in enumerate(CLASES):
    carpeta_clase=os.path.join(RUTA_BASE,clase)
    archivos=[f for f in os.listdir(carpeta_clase) if f.endswith('.jpg')]

    random.shuffle(archivos)
    split_idx=int(len(archivos)*DIV_ENTRENAMIENTO)

    for i, archivo_img in enumerate(archivos):
        conjunto='train' if i<split_idx else 'val'

        ruta_img_origen=os.path.join(carpeta_clase,archivo_img)
        ruta_txt_origen=os.path.join(carpeta_clase,archivo_img.replace('.jpg','.txt'))

        ruta_img_destino=os.path.join(RUTA_DATASET,conjunto,'images',archivo_img)
        ruta_txt_destino=os.path.join(RUTA_DATASET,conjunto,'labels',archivo_img.replace('.jpg','.txt'))

        shutil.copy(ruta_img_origen,ruta_img_destino)
        if os.path.exists(ruta_txt_origen):
            shutil.copy(ruta_txt_origen,ruta_txt_destino)
        else:
            print(f"No se encontro etiqueta para: {archivo_img}")

print("Imagenes y etiquetas divididas correctamente..")

#Creacion de archivo YAMAL
yaml_data={
    'train': os.path.abspath(os.path.join(RUTA_DATASET,'train','images')).replace('\\','/'),
    'val': os.path.abspath(os.path.join(RUTA_DATASET,'val','images')).replace('\\','/'),
    'nc': len(CLASES),
    'names': CLASES
}

ruta_yaml=os.path.join(RUTA_DATASET,'objetos.yaml')
with open(ruta_yaml,'w') as f:
    yaml.dump(yaml_data,f,sort_keys=False)

print("Archivo YAML creado correctamene")
print(ruta_yaml)
print(yaml.dump(yaml_data,sort_keys=False))