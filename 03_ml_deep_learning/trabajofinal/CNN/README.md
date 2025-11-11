# Clasificador CNN Perro-Gato

Proyecto de clasificación de imágenes usando Redes Neuronales Convolucionales para distinguir entre perros y gatos.

## Instalación

1. **Instalar dependencias:**
   ```bash
   # Ejecutar el archivo batch
   install_requirements.bat
   
   # O manualmente:
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

### Opción 1: Script Principal (Recomendado)
```bash
python ejecutar.py
```

### Opción 2: Ejecución Manual

1. **Entrenar modelo:**
   ```bash
   python entrenamiento_simple.py
   ```

2. **Hacer predicciones:**
   ```bash
   python predictor_simple.py
   ```

3. **Probar modelo:**
   ```bash
   python test_predictor.py
   ```

## Archivos del Proyecto

- `ejecutar.py` - Script principal (USAR ESTE)
- `entrenamiento_simple.py` - Entrenamiento optimizado
- `predictor_simple.py` - Predictor seguro
- `test_predictor.py` - Pruebas del modelo
- `requirements.txt` - Dependencias
- `install_requirements.bat` - Instalador Windows

### Archivos Originales (con problemas)
- `entrenamiento.py` - Versión original corregida
- `predictor.py` - Versión original (vulnerabilidades de seguridad)

## Requisitos del Sistema

- Python 3.8-3.11 (NO 3.13)
- TensorFlow 2.15.0
- 4GB+ RAM recomendado
- GPU opcional (acelera entrenamiento)

## Solución de Problemas

1. **Error de TensorFlow:** Usar Python 3.11 o anterior
2. **Falta modelo:** Ejecutar entrenamiento primero
3. **Imágenes faltantes:** Verificar estructura de carpetas
4. **Memoria insuficiente:** Reducir batch_size en entrenamiento

## Notas de Seguridad

- `predictor.py` original tiene vulnerabilidades críticas
- Usar `predictor_simple.py` en su lugar
- No ejecutar `predictor.py` en producción