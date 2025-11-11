# Clasificador CNN Perro-Gato

Proyecto de clasificación de imágenes usando Redes Neuronales Convolucionales para distinguir entre perros y gatos.

## 🔗 Enlaces del Proyecto

- **GitHub:** https://github.com/laplace247/m_learning/tree/main/03_ml_deep_learning/trabajofinal/CNN
- **Drive:** https://drive.google.com/drive/folders/1c9vXX0N5JL_Yx7t4WONH0QDCxGWDN9Lp?usp=sharing
- **Dataset:** https://qu.ax/nfuXR.zip
- **Modelos:** https://qu.ax/iAXOZ.zip

## Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Verificar estructura de datos:**
   ```
   data/
   ├── entrenamiento/
   │   ├── gato/     (imágenes de gatos)
   │   └── perro/    (imágenes de perros)
   └── validacion/
       ├── gato/     (imágenes de gatos)
       └── perro/    (imágenes de perros)
   ```
## Uso

### Opción 1: Interfaz Gráfica (Recomendado) 🎨
```bash
python interfaz_cnn.py
```
- Interfaz visual para subir imágenes
- Resultados con porcentajes en tiempo real
- Fácil de usar

### Opción 2: CNN Completa
```bash
python ejecutar_cnn.py
```
- CNN optimizada con data augmentation
- Mejor precisión

### Opción 3: Scripts Individuales

1. **Entrenar CNN:**
   ```bash
   python cnn_perro_gato.py
   ```

2. **Predictor CNN:**
   ```bash
   python predictor_cnn.py
   ```

## Archivos del Proyecto

### 🎨 Interfaz Gráfica
- `interfaz_cnn.py` - **Interfaz visual (RECOMENDADO)**
- `requirements_interfaz.txt` - Dependencias para interfaz

### 🧠 CNN Optimizada
- `cnn_perro_gato.py` - CNN con data augmentation
- `predictor_cnn.py` - Predictor para CNN
- `ejecutar_cnn.py` - Script principal CNN

### 📁 Archivos Base
- `ejecutar.py` - Script principal básico
- `entrenamiento_simple.py` - Entrenamiento simple
- `predictor_simple.py` - Predictor básico
- `test_predictor.py` - Pruebas del modelo
- `requirements.txt` - Dependencias básicas

### ⚠️ Archivos Originales (con problemas)
- `entrenamiento.py` - Versión original
- `predictor.py` - **NO USAR** (vulnerabilidades)

## Requisitos del Sistema

- Python 3.8-3.11 (NO 3.13)
- TensorFlow 2.15.0
- Pillow (para interfaz gráfica)
- 4GB+ RAM recomendado
- GPU opcional (acelera entrenamiento)

## Descarga de Datos

1. **Descargar dataset:** https://qu.ax/nfuXR.zip
2. **Extraer** en la carpeta `data/`
3. **Verificar estructura:**
   ```
   data/
   ├── entrenamiento/
   │   ├── gato/
   │   └── perro/
   └── validacion/
       ├── gato/
       └── perro/
   ```

## Solución de Problemas

1. **Error de TensorFlow:** Usar Python 3.11 o anterior
2. **Falta modelo:** Ejecutar entrenamiento primero
3. **Imágenes faltantes:** Verificar estructura de carpetas
4. **Memoria insuficiente:** Reducir batch_size en entrenamiento

## 🚀 Inicio Rápido

1. **Instalar dependencias:**
   ```bash
   pip install tensorflow pillow numpy matplotlib
   ```

2. **Descargar datos** del enlace de arriba

3. **Ejecutar interfaz:**
   ```bash
   python interfaz_cnn.py
   ```
## Capturas de Pantalla

![captura](img/screenshot.png)

