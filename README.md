# FeriadeBarrio
Este es un **demo funcional** del proyecto de arquitectura de sistemas informáticos para una feria de barrio.

### Origen del proyecto
- **Diseño original:** AppSheet (frontend) + Supabase (backend PostgreSQL)
- **Problema detectado:** El plan gratuito de AppSheet no permite conexión directa con PostgreSQL
- **Solución implementada:** Migración del frontend a **Streamlit** (Python), manteniendo la base de datos en la nube

### Tecnologías actuales
| Componente | Tecnología |
|------------|------------|
| Frontend | Streamlit |
| Base de datos | Neon (PostgreSQL) |

*La base de datos original de Supabase se migró a Neon conservando la misma estructura de tablas y triggers.*

### ¿Por qué funcionó?
- **Neon** permite conexión directa y SSL sin restricciones
- **Streamlit** es gratuito y se despliega fácilmente en la nube
- La estructura SQL (tablas y trigger) se reutilizó sin cambios
- clave feriante:feriante2026
- clave ayudantes:
- "Pedro":pedro2026
  "Maria":maria2026
  "Jose":jose2026

---

## 🚀 **Despliegue en Neon (PostgreSQL) - Paso a Paso**

### 📋 **Paso 1: Instalar Streamlit en Visual Studio Code**

```bash
# Abre terminal en VS Code (Ctrl+ñ)
pip install streamlit
```

### 📋 **Paso 2: Crear archivos del proyecto**

| Archivo | ¿Subir a GitHub? |
|---------|------------------|
| `app.py` | ✅ Sí |
| `requirements.txt` | ✅ Sí |
| `db_config.py` | ✅ Sí |
| `.env` | ❌ **NO** |

### ✅ **Paso 3: Verificación local**

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py
```

> La app debe funcionar en `localhost` antes de continuar.

### ☁️ **Paso 4: Despliegue en Streamlit Cloud**

1. **Sube a GitHub** (solo `app.py`, `requirements.txt`, `db_config.py`)

2. **Ve a [share.streamlit.io](https://share.streamlit.io)** y conecta tu repositorio

3. **Configura Secrets** (Advanced settings → Secrets):

```toml
DATABASE_URL = "postgresql://usuario:contraseña@host.neon.tech/dbname"
```

4. **Click en Deploy** 🚀

### ⚠️ **Importante**

| Requisito | Neon |
|-----------|------|
| Whitelist IP | ✅ Necesitas agregar IPs de Streamlit |
| `.env` a GitHub | ❌ No subir |
| Secrets configurados | ✅ Obligatorio |



## 📊 Comparativa Técnica: Neon vs Supabase

| Aspecto | 🔷 Neon | 🔶 Supabase |
|---------|---------|-------------|
| **Biblioteca Python** | `psycopg2-binary` | `supabase` |
| **Cadena de conexión** | `postgresql://user:pass@host/db` | URL + anon key |
| **Trigger** | ✅ En BD (PL/pgSQL) | ✅ En BD (PL/pgSQL) |
| **Descuento de stock** | ✅ Automático (trigger) | ✅ Automático (trigger) |
| **Configuración en Cloud** | Requiere whitelist IP | Sin configuración extra |
| **Dificultad** | Media | Baja |

> **Conclusión:** Ambos funcionan igual. La diferencia está en la facilidad de despliegue.
> ## ⚠️ **Neon: Se suspende a los 5 minutos sin uso**
- ⏱️ Si no hay consultas en **5 minutos**, la BD se duerme
- 🔄 Al vender de nuevo, tarda **2-5 segundos** en reactivarse
- 💰 Solo un **plan de pago** desactiva esta pausa automática

#para probar la conexion pegar el enlace en la barra de direcciones

#del navegador:https://h7e8ujqlyl2rq2muptrwrm.streamlit.app/
