# Solución de Problemas - Sistema IA Personal Paraguay

## 🚨 Problemas Críticos Sistema IA y Soluciones

### **🔴 CRÍTICO: "OpenAI API key es requerida para esta aplicación IA"**

#### **🔍 Síntoma**
- La aplicación se detiene completamente al cargar
- Error rojo prominente sobre API key faltante
- Mensaje: "Esta aplicación requiere sistema IA funcional"
- No hay acceso a ninguna funcionalidad

#### **🔧 Causa Raíz**  
- Sistema IA puro requiere OpenAI obligatorio
- API key no configurada en .env o Streamlit secrets
- Variable de entorno OPENAI_API_KEY no disponible
- Key inválida o expirada

#### **✅ Solución - Desarrollo Local**
```bash
# 1. Crear/editar archivo .env en directorio raíz:
echo "OPENAI_API_KEY=sk-proj-tu-api-key-real" > .env

# 2. Verificar archivo creado correctamente
cat .env

# 3. Reiniciar aplicación completamente:
streamlit run streamlit_app.py
```

#### **✅ Solución - Streamlit Cloud**
1. **Dashboard**: Ir a Streamlit Cloud → tu aplicación
2. **Secrets**: Settings → Secrets → Advanced settings  
3. **Configurar**:
```toml
# Agregar en secrets:
OPENAI_API_KEY = "sk-proj-tu-api-key-openai"
```
4. **Redeploy**: Save → Reboot app

#### **🔍 Verificación Exitosa**
- ✅ Página principal: "✅ Sistema IA Maestro: Activo y Funcional"
- ✅ Métricas: "🤖 GPT-4 Listo" visible  
- ✅ Info: "🧠 Sistema configurado para análisis IA avanzado"

---

### **Error: "Sistema IA no está disponible"**

#### **Síntoma**
- Botón "Analizar con IA" no hace nada
- Mensaje de error al hacer clic
- Sistema parece cargado pero análisis falla

#### **Causa Raíz**
- `caso_uso_maestro` no se inicializó correctamente
- Problemas en dependency injection
- AnalizadorMaestroIA no disponible

#### **Solución**
1. **Recarga la página completa** (F5)
2. **Verifica logs** en Streamlit Cloud:
   ```
   Buscar: "AnalizadorMaestroIA inicializado"
   Buscar: "Error configurando AnalizadorMaestroIA"
   ```
3. **Verifica API key validity**:
   - Loguéate en OpenAI platform
   - Verifica que la API key no esté revocada
   - Verifica que tengas créditos disponibles

#### **Verificación**
- Sistema debe inicializar sin errores
- Logs deben mostrar: "AnalizadorMaestroIA configurado exitosamente"

---

### **Error: "Error de servicio IA" durante análisis**

#### **Síntoma**  
- Archivo sube correctamente
- Análisis comienza pero falla
- Error específico de OpenAI

#### **Causas Comunes**

##### **Rate Limit Exceeded**
```
Error: Rate limit reached for requests
```
**Solución**: Espera 1-2 minutos y reintenta

##### **Insufficient Credits**
```
Error: You exceeded your current quota
```
**Solución**: Agregar créditos a cuenta OpenAI

##### **Invalid API Key**
```
Error: Incorrect API key provided
```
**Solución**: Verificar/regenerar API key en OpenAI

##### **Model Not Available**
```
Error: The model gpt-4 does not exist
```
**Solución**: Verificar acceso a GPT-4 en tu cuenta OpenAI

#### **Diagnóstico**
```python
# Para diagnosticar, busca en logs:
"🤖 AnalizadorMaestroIA inicializado"     # ← Debe aparecer
"📡 Calling OpenAI API"                   # ← Debe aparecer  
"✅ OpenAI API successful"                # ← Si falla aquí = problema API
```

---

### **Error: "Archivo muy grande. Máximo 5MB"**

#### **Síntoma**
- Error inmediato al subir archivo
- No se puede proceder con análisis

#### **Soluciones**

##### **Reducir Tamaño de Archivo**
1. **Eliminar columnas innecesarias**: Mantén solo comentarios + NPS/Nota
2. **Filtrar filas vacías**: Elimina filas sin comentarios
3. **Guardar como Excel comprimido**: Usar "Save as" → Excel optimized

##### **Dividir Análisis**
1. **Separar en archivos más pequeños**: 1000-1500 comentarios por archivo
2. **Analizar por lotes**: Combinar resultados manualmente  
3. **Priorizar datos**: Analizar primero comentarios más recientes/importantes

##### **Optimización de Datos**
```excel
# ANTES: Archivo pesado
Comentario | Fecha | Cliente | Email | Teléfono | NPS | Nota | Categoría | ...

# DESPUÉS: Archivo optimizado  
Comentario | NPS | Nota
```

---

### **Error: "No se pudo generar vista previa"**

#### **Síntoma**
- Archivo sube pero no muestra vista previa
- Warning sobre formato incorrecto

#### **Causas y Soluciones**

##### **Formato de Archivo Incorrecto**
```
Formatos soportados: .xlsx, .xls, .csv únicamente
```
**Solución**: Convertir archivo al formato correcto

##### **Archivo Corrupto**
**Solución**: 
1. Abre archivo en Excel/Google Sheets
2. "Guardar como" nuevo archivo  
3. Intenta subir el nuevo archivo

##### **Encoding Incorrecto (CSV)**
**Solución**: 
1. Abrir CSV en editor de texto
2. Guardar con encoding UTF-8
3. O convertir a Excel

---

### **Error: "Error inesperado"**

#### **Síntoma**  
- Error genérico sin causa específica
- Aplicación falla en lugar inesperado

#### **Pasos de Diagnóstico**
1. **Recarga página completa** (F5)
2. **Intenta con archivo más pequeño** (5-10 comentarios)
3. **Verifica formato de comentarios**: ¿Tienen texto válido?
4. **Check browser console**: F12 → Console → busca errores JavaScript

#### **Escalación a Soporte**
Si el problema persiste:
1. **Documenta pasos exactos** para reproducir
2. **Incluye archivo de muestra** (sin datos sensibles)
3. **Screenshot del error** específico
4. **Información del browser** (Chrome, Firefox, etc.)

---

## 🔧 Problemas de Performance

### **Análisis muy lento (>2 minutos)**

#### **Causas**
- **Archivo muy grande**: >1000 comentarios
- **Comentarios muy largos**: Más tokens = más tiempo
- **Rate limiting**: OpenAI limita requests

#### **Soluciones**
1. **Reducir tamaño**: Máximo 500 comentarios por análisis
2. **Comentarios más cortos**: Truncar a 200 caracteres si necesario
3. **Análisis secuencial**: Esperar entre análisis múltiples

### **App se congela durante análisis**

#### **Causa**
- Browser timeout
- Conexión interrumpida
- Memory issues

#### **Soluciones** 
1. **No cambiar de pestaña** durante análisis
2. **Mantener browser abierto** hasta completar
3. **Clear browser cache** si se comporta extraño
4. **Usar browser actualizado** (Chrome/Firefox última versión)

---

## 📊 Validación de Resultados

### **¿Los resultados se ven correctos?**

#### **Métricas Esperadas**
- **Total comentarios**: Debe coincidir con filas de tu archivo
- **Sentimientos**: Suma debe aproximarse al total
- **Tiempo IA**: 0.5-2.0 segundos por cada 100 comentarios típicamente

#### **Insights de Calidad**
- **Temas detectados**: Deben ser relevantes a tu industria
- **Emociones**: Deben hacer sentido con contenido de comentarios
- **Resumen ejecutivo**: Debe sonar coherente y específico
- **Recomendaciones**: Deben ser accionables y específicas

#### **Red Flags**
- **Cero temas detectados**: Posible problema con contenido
- **Todas emociones iguales**: Posible problema con variedad
- **Resumen muy genérico**: Posible problema con prompt
- **Cero críticos en dataset negativo**: Posible problema con detection

---

## 🎯 Optimización de Uso

### **Para Mejores Resultados IA**
1. **Comentarios completos**: Frases completas > palabras sueltas
2. **Variedad de contenido**: Mix de positivos/negativos da mejor análisis
3. **Contexto relevante**: Comentarios sobre mismo tema/servicio
4. **Idioma consistente**: Evitar mezclar idiomas en mismo análisis

### **Para Performance Óptima**
1. **Archivos optimizados**: Solo columnas necesarias
2. **Batch sizes**: 100-500 comentarios = sweet spot
3. **Horarios valle**: Usar durante horas de menos tráfico OpenAI
4. **Cache utilization**: Re-análisis de mismos datos usa cache

---

## 📞 Escalación y Contacto

### **Nivel 1: Auto-resolución**
- Revisar esta guía
- Recargar página
- Verificar archivo format

### **Nivel 2: Troubleshooting Avanzado**
- Verificar configuración OpenAI
- Clear cache y cookies
- Testing con archivo minimal

### **Nivel 3: Soporte Técnico**
- Contactar administrador del sistema
- Proporcionar logs y screenshots
- Incluir archivo de muestra para debugging

---

*Guía de troubleshooting v3.0.0-ia-pure*  
*Sistema IA Puro | Personal Paraguay | 2025*