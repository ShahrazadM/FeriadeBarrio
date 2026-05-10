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
