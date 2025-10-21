from ultralytics import YOLO
import os

ruta_base=r"C:\Users\Estudiante\Downloads\sem05"
ruta_yaml=os.path.join(ruta_base,"data","dataset","objetos.yaml")

os.chdir(ruta_base)

ruta_yolo=r"C:\Users\Estudiante\Downloads\sem05\yolov8n.pt"
model=YOLO(ruta_yolo)

#Entrenar modelo
results=model.train(
    data=ruta_yaml,
    epochs=50,
    imgsz=640,
    batch=8,
    name="objetos",
    device='cpu'   #cuda -- tarjeta video
)

print("Entrenamiento completado correctamente..")
print("Los resultados se guardaron en:")
print(os.path.join(ruta_base,"runs","detect","objetos"))
print("Dentro encontrarás el archivo 'best.pt' (Modelo entrenado)")