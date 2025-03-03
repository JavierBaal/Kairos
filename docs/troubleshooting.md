# Guía de Solución de Problemas - Kairos

## Herramientas de Diagnóstico

### 1. Diagnóstico del Sistema
Para ejecutar un diagnóstico completo del sistema:
```batch
cd run_scripts
python diagnostics.py
```
Este comando generará un reporte detallado que incluye:
- Información del sistema operativo
- Versión de Python
- Dependencias instaladas
- Estado de PyQt6
- Estructura del proyecto
- Disponibilidad de fuentes

### 2. Verificación del Sistema
Para verificar la integridad básica del sistema:
```batch
cd run_scripts
python check_system.py
```
Verifica:
- Versión de Python
- Dependencias críticas
- Estructura de archivos
- Plugins de Qt

## Problemas Comunes y Soluciones

### 1. Problemas con PyQt6

#### Síntomas:
- La aplicación no se inicia
- Errores relacionados con QtWidgets
- Plugins no encontrados

#### Soluciones:
1. Reiniciar el entorno:
   ```batch
   run_scripts/reset_environment.bat
   ```
2. Instalar manualmente:
   ```batch
   pip install --no-cache-dir PyQt6==6.6.1 PyQt6-Qt6==6.6.1 PyQt6-sip==13.6.0
   ```

### 2. Problemas de Fuentes

#### Síntomas:
- Fuentes no se ven correctamente
- Advertencia sobre la fuente Inter

#### Soluciones:
1. Instalar la fuente Inter desde:
   https://fonts.google.com/specimen/Inter
2. Usar fuentes del sistema (automático)
3. Verificar la instalación:
   ```batch
   cd run_scripts
   python diagnostics.py
   ```

### 3. Problemas de Estructura del Proyecto

#### Síntomas:
- Errores de importación
- Módulos no encontrados

#### Soluciones:
1. Verificar estructura:
   ```batch
   cd run_scripts
   python check_system.py
   ```
2. Si hay problemas, usar el reinicio del entorno:
   ```batch
   run_scripts/reset_environment.bat
   ```

### 4. Problemas de Dependencias

#### Síntomas:
- Errores de importación
- Versiones incompatibles

#### Soluciones:
1. Reinstalar dependencias:
   ```batch
   install.bat
   ```
2. Limpieza completa:
   ```batch
   run_scripts/reset_environment.bat
   ```

## Reporte de Diagnóstico

El reporte de diagnóstico se guarda en:
```
run_scripts/diagnostic_report.json
```

Contiene información detallada sobre:
- Estado del sistema
- Dependencias instaladas
- Configuración de PyQt
- Estructura del proyecto
- Fuentes disponibles

## Pasos de Recuperación

Si la aplicación no funciona:

1. **Diagnóstico**
   ```batch
   cd run_scripts
   python diagnostics.py
   ```

2. **Verificación**
   ```batch
   python check_system.py
   ```

3. **Reinicio del Entorno**
   ```batch
   reset_environment.bat
   ```

4. **Reinstalación Limpia**
   - Desinstalar todas las dependencias
   - Ejecutar `install.bat`
   - Verificar con `diagnostics.py`

## Contacto y Soporte

Si los problemas persisten:
1. Revisar el reporte de diagnóstico
2. Verificar los requisitos del sistema
3. Contactar al equipo de soporte con el reporte de diagnóstico

## Requisitos del Sistema

- Python 3.8 o superior
- Windows 10/11
- 4GB RAM mínimo
- Conexión a Internet para instalación inicial
