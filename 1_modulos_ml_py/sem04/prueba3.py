import cv2
import os
import smtplib
from email.message import EmailMessage
from sklearn.ensemble import RandomForestClassifier

email_emisor = "fduilioomarquispe@gmail.com"
email_password = "rlot ybep mzur ykdr"
email_receptor = "floresquispeomar8@gmail.com"

ruta_capturas = "capturas_alerta" # carpeta de capturas
movimientos_alerta = 80  # nro de mov detectados

def enviar_correo_con_adjunto(ruta_imagen):
    print(f"Preparando correo para {email_receptor}...")

    mensaje = EmailMessage()
    mensaje["From"] = email_emisor
    mensaje["To"] = email_receptor
    mensaje["Subject"] = "¡Alerta de Movimiento Detectado!"
    
    nombre_archivo = os.path.basename(ruta_imagen)
    mensaje.set_content(f"Se ha detectado movimiento.\nSe adjunta captura: {nombre_archivo}")

    # Adjuntar la imagen
    with open(ruta_imagen, "rb") as f:
        mensaje.add_attachment(
            f.read(),
            maintype="image",
            subtype="jpeg",
            filename=nombre_archivo
        )
    # Enviar el correo
    try:
        cliente_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        cliente_smtp.starttls()
        cliente_smtp.login(email_emisor, email_password)
        cliente_smtp.send_message(mensaje)
        cliente_smtp.quit()
        print("Correo de alerta enviado exitosamente.")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al enviar el correo: {e}")

# Entrenar clasificador
x_train = [[100], [300], [500], [700], [900], [5000], [7000], [9000], [12000]]
y_train = ['pequeno'] * 5 + ['grande'] * 4
clf = RandomForestClassifier()
clf.fit(x_train, y_train)

# Asegurar que la carpeta de capturas exista
os.makedirs(ruta_capturas, exist_ok=True)

# Iniciar cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

ret, frame1 = cap.read()
frame1_gray = cv2.GaussianBlur(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), (21, 21), 0)
conteo_mov = 0

# Bucle principal
while True:
    ret, frame2 = cap.read()
    if not ret:
        break

    gray = cv2.GaussianBlur(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    delta = cv2.absdiff(frame1_gray, gray)
    thresh = cv2.dilate(cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    texto_pred = "Sin movimiento"
    
    for contour in contours:
        # filtra pequeños movimientos
        if cv2.contourArea(contour) < 500:
            continue

        conteo_mov += 1
        
        area = cv2.contourArea(contour)
        prediction = clf.predict([[area]])[0]
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        texto_pred = f"Movimiento: {prediction} | Area: {int(area)}"
        
        # Comprobar si el conteo es un múltiplo de 80 y no es cero
        if conteo_mov % movimientos_alerta == 0 and conteo_mov > 0:
            # Guardar la imagen
            nombre_foto = f"alerta_{conteo_mov}.jpg"
            direccion_foto = os.path.join(ruta_capturas, nombre_foto)
            cv2.imwrite(direccion_foto, frame2)
            print(f"Límite alcanzado ({conteo_mov} mov.). Captura guardada.")

            # Enviar el correo con la imagen
            enviar_correo_con_adjunto(direccion_foto)
        break

    # Mostrar información en pantalla
    cv2.putText(frame2, texto_pred, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame2, f"Conteo de Movimientos: {conteo_mov}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Mostrar ventanas y actualizar frame base
    cv2.imshow("Sistema de Vigilancia", frame2)
    frame1_gray = gray.copy()

    if cv2.waitKey(30) & 0xFF == 27:
        print("Saliendo del programa.")
        break
# Salir de la captura de video
cap.release()
cv2.destroyAllWindows()