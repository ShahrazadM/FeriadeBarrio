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
#para probar la conexion pegar el enlace en la barra de direcciones
#del navegador:https://h7e8ujqlyl2rq2muptrwrm.streamlit.app/
