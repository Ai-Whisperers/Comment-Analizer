# 🌩️ Streamlit Cloud Emulator

## ¿Qué es esto?

Este directorio contiene un **emulador completo del entorno de Streamlit Cloud** para desarrollo local. 

🎯 **Objetivo:** Desarrollar y probar localmente con exactamente las mismas limitaciones y configuraciones que tendrás en producción.

## 🚨 Diferencias críticas que emula

| Recurso | Tu Local | Streamlit Cloud | Este Emulador |
|---------|----------|-----------------|---------------|
| **Memoria RAM** | Ilimitada | **1GB** | **1GB** ✅ |
| **CPU** | Todos los cores | **Limitado** | **1 CPU** ✅ |
| **Configuración** | `.env` | `secrets.toml` | **Ambos** ✅ |
| **Python** | 3.12.6 | 3.12 | **3.12** ✅ |
| **Límites** | Sin límites | Estrictos | **Estrictos** ✅ |

## 🚀 Cómo usar

### 1. Iniciar el emulador
```bash
cd streamlit-cloud-emulator
python emulator.py --start
```

### 2. Detener el emulador  
```bash
python emulator.py --stop
```

### 3. Ver logs del emulador
```bash
python emulator.py --logs
```

### 4. Reiniciar (equivale a reboot en Streamlit Cloud)
```bash
python emulator.py --restart
```

## 📊 Monitoreo de recursos

El emulador incluye monitoreo en tiempo real que muestra:
- ✅ Uso de memoria (máx 1GB)
- ✅ Uso de CPU (máx 1 core) 
- ✅ Número de usuarios concurrentes
- ✅ Cache size
- ⚠️ Alertas cuando te acercas a los límites

## 🔧 Archivos incluidos

- `Dockerfile` - Imagen Docker que replica Streamlit Cloud
- `docker-compose.yml` - Configuración con límites exactos  
- `emulator.py` - Script principal de gestión
- `monitor.py` - Monitoreo de recursos en tiempo real
- `cloud-config.py` - Configuración específica para emular cloud

## ⚠️ Importante

**NO MODIFICAR** los límites de recursos en `docker-compose.yml`. 

Están configurados para replicar exactamente Streamlit Cloud:
- `mem_limit: 1g` 
- `cpus: 1.0`

Si tu app funciona aquí, funcionará en Streamlit Cloud. Si falla aquí, fallará allá también.

## 🎯 Casos de uso

✅ **Antes de hacer deploy** - Asegúrate que funciona con límites reales  
✅ **Debugging** - Reproduce errores de producción localmente  
✅ **Performance testing** - Ve cómo se comporta con recursos limitados  
✅ **Multi-user testing** - Simula múltiples usuarios concurrentes