import streamlit as st
import pandas as pd
import plotly.express as px
import time
from db_config import get_connection

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(page_title="Feria de Barrio - Neon", page_icon="⚡", layout="wide")

st.title("⚡ Feria de Barrio - Gestor de Ventas")
st.caption("🚀 Base de datos: **Neon (PostgreSQL) - Conexión Rápida**")

# ============================================
# SISTEMA DE ROLES (Feriante / Ayudante)
# ============================================

# Inicializar session_state
if 'rol' not in st.session_state:
    st.session_state.rol = "ayudante"
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = "Ayudante"

def autenticar_feriante():
    if st.session_state.clave_feriante == "feriante2026":
        st.session_state.autenticado = True
        st.session_state.rol = "feriante"
        st.session_state.usuario = "Feriante (Dueño)"
    else:
        st.error("❌ Contraseña incorrecta")

def cambiar_a_ayudante():
    st.session_state.autenticado = False
    st.session_state.rol = "ayudante"
    st.session_state.usuario = "Ayudante"

# Barra lateral para autenticación
with st.sidebar:
    st.header("👤 Control de Acceso")
    
    if st.session_state.rol == "feriante":
        st.success(f"✅ **{st.session_state.usuario}**")
        st.caption("Acceso: TOTAL (Inventario, Ventas, Reportes, Mermas)")
        if st.button("🔓 Cambiar a Modo Ayudante", use_container_width=True):
            cambiar_a_ayudante()
    else:
        st.info("👤 **Modo Ayudante**")
        st.caption("Acceso: Solo registro de ventas y reportes")
        
        st.markdown("---")
        st.subheader("🔐 Acceso Feriante")
        st.caption("Si eres el dueño, ingresa tu contraseña:")
        st.text_input("Contraseña", type="password", key="clave_feriante", on_change=autenticar_feriante)
        st.caption("Contraseña de prueba: `feriante2026`")

st.markdown("---")

# ============================================
# FUNCIONES DE BASE DE DATOS
# ============================================

@st.cache_data(ttl=10)
def get_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio_por_kilo, stock_kg FROM productos ORDER BY nombre")
    productos_raw = cur.fetchall()
    cur.close()
    conn.close()
    
    productos = []
    for p in productos_raw:
        productos.append((p[0], p[1], float(p[2]), float(p[3])))
    return productos

def registrar_venta(feriante_email, total, tipo_pago):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ventas (feriante_email, total, tipo_pago)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (feriante_email, total, tipo_pago))
    venta_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return venta_id

def registrar_detalle(venta_id, producto_id, cantidad_kg, precio_por_kilo, subtotal):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO venta_detalles (venta_id, producto_id, cantidad_kg, precio_por_kilo, subtotal)
        VALUES (%s, %s, %s, %s, %s)
    """, (venta_id, producto_id, cantidad_kg, precio_por_kilo, subtotal))
    conn.commit()
    cur.close()
    conn.close()

def registrar_merma(producto_id, cantidad_kg, email, motivo):
    """Registra una merma (pérdida de producto)"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO ventas (feriante_email, total, tipo_pago, observacion)
        VALUES (%s, 0, 'merma', %s)
        RETURNING id
    """, (email, motivo))
    venta_id = cur.fetchone()[0]
    
    cur.execute("""
        INSERT INTO venta_detalles (venta_id, producto_id, cantidad_kg, precio_por_kilo, subtotal)
        VALUES (%s, %s, %s, 0, 0)
    """, (venta_id, producto_id, cantidad_kg))
    
    conn.commit()
    cur.close()
    conn.close()
    return venta_id

@st.cache_data(ttl=30)
def get_ventas_semanales():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            DATE(v.fecha) as fecha,
            p.nombre as producto,
            vd.cantidad_kg,
            vd.subtotal,
            v.tipo_pago
        FROM ventas v
        JOIN venta_detalles vd ON v.id = vd.venta_id
        JOIN productos p ON vd.producto_id = p.id
        WHERE v.fecha >= NOW() - INTERVAL '7 days'
        AND v.tipo_pago != 'merma'
        ORDER BY v.fecha DESC
    """)
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    
    if ventas:
        df = pd.DataFrame(ventas, columns=['fecha', 'producto', 'cantidad_kg', 'subtotal', 'tipo_pago'])
        df['cantidad_kg'] = df['cantidad_kg'].astype(float)
        df['subtotal'] = df['subtotal'].astype(float)
        return df
    return pd.DataFrame()

@st.cache_data(ttl=30)
def get_mermas_semanales():
    """Obtiene las mermas de los últimos 7 días (solo para feriante)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            DATE(v.fecha) as fecha,
            p.nombre as producto,
            vd.cantidad_kg,
            v.observacion
        FROM ventas v
        JOIN venta_detalles vd ON v.id = vd.venta_id
        JOIN productos p ON vd.producto_id = p.id
        WHERE v.fecha >= NOW() - INTERVAL '7 days'
        AND v.tipo_pago = 'merma'
        ORDER BY v.fecha DESC
    """)
    mermas = cur.fetchall()
    cur.close()
    conn.close()
    
    if mermas:
        df = pd.DataFrame(mermas, columns=['fecha', 'producto', 'cantidad_kg', 'motivo'])
        df['cantidad_kg'] = df['cantidad_kg'].astype(float)
        return df
    return pd.DataFrame()

# ============================================
# INTERFAZ SEGÚN EL ROL
# ============================================

if st.session_state.rol == "feriante":
    # ==================== FERIANTE: ACCESO TOTAL ====================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📦 Inventario", "💰 Registrar Venta", "📊 Reporte Semanal", "⚠️ Mermas", "⚙️ Configuración"])
    
    # ----- TAB 1: INVENTARIO -----
    with tab1:
        st.header("📦 Inventario Actual")
        productos = get_productos()
        
        if productos:
            df = pd.DataFrame(productos, columns=['id', 'nombre', 'precio_por_kilo', 'stock_kg'])
            df['precio_por_kilo'] = df['precio_por_kilo'].apply(lambda x: f"${x:,.0f}/kg")
            df['stock_kg'] = df['stock_kg'].apply(lambda x: f"{x:.1f} kg")
            st.dataframe(df[['nombre', 'precio_por_kilo', 'stock_kg']], use_container_width=True)
            
            # Stock bajo
            stock_bajo = [p for p in productos if p[3] < 10]
            if stock_bajo:
                st.warning("⚠️ **Productos con stock bajo (< 10 kg):**")
                for p in stock_bajo:
                    st.write(f"- {p[1]}: {p[3]:.1f} kg")
        else:
            st.info("📭 No hay productos cargados")
    
    # ----- TAB 2: REGISTRAR VENTA (también para ayudante, pero aquí está) -----
    with tab2:
        st.header("💰 Nueva Venta")
        productos = get_productos()
        
        if productos:
            opciones = {p[1]: {'id': p[0], 'precio': p[2], 'stock': p[3]} for p in productos}
            nombres = list(opciones.keys())
            
            if 'producto_venta' not in st.session_state:
                st.session_state.producto_venta = nombres[0] if nombres else None
            if 'cantidad_venta' not in st.session_state:
                st.session_state.cantidad_venta = 0.5
            
            col1, col2 = st.columns(2)
            
            with col1:
                tipo_pago = st.selectbox("💳 Tipo de pago", ["efectivo", "tarjeta"])
                producto = st.selectbox("🍎 Producto", nombres, key="select_venta")
                st.session_state.producto_venta = producto
            
            with col2:
                cantidad = st.number_input("⚖️ Cantidad (kg)", min_value=0.1, step=0.1, format="%.1f", 
                                          value=st.session_state.cantidad_venta, key="input_venta")
                st.session_state.cantidad_venta = cantidad
                email = st.text_input("📧 Email", value="prueba@ejemplo.com")
            
            if producto:
                precio = opciones[producto]['precio']
                stock = opciones[producto]['stock']
                subtotal = cantidad * precio
                st.info(f"💰 Precio por kg: ${precio:,.0f} | 📦 Stock: {stock:.1f} kg")
                st.metric("💵 Subtotal", f"${subtotal:,.0f}")
                
                if st.button("✅ Registrar Venta", use_container_width=True):
                    if cantidad <= stock:
                        venta_id = registrar_venta(email, subtotal, tipo_pago)
                        registrar_detalle(venta_id, opciones[producto]['id'], cantidad, precio, subtotal)
                        st.success(f"✅ Venta registrada! {cantidad} kg de {producto}")
                        st.balloons()
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Stock insuficiente. Solo hay {stock:.1f} kg")
        else:
            st.info("📭 No hay productos cargados")
    
    # ----- TAB 3: REPORTE SEMANAL -----
    with tab3:
        st.header("📊 Reporte de Ventas - Última Semana")
        
        df_ventas = get_ventas_semanales()
        
        if not df_ventas.empty:
            ventas_dia = df_ventas.groupby('fecha')['subtotal'].sum().reset_index()
            fig = px.bar(ventas_dia, x='fecha', y='subtotal', title="💰 Ventas por Día", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
            top_productos = df_ventas.groupby('producto')['cantidad_kg'].sum().reset_index()
            top_productos = top_productos.sort_values('cantidad_kg', ascending=False)
            fig2 = px.bar(top_productos, x='producto', y='cantidad_kg', title="📦 Kilos por Producto", text_auto=True)
            st.plotly_chart(fig2, use_container_width=True)
            
            pago_dist = df_ventas.groupby('tipo_pago').size().reset_index(name='cantidad')
            if not pago_dist.empty:
                fig3 = px.pie(pago_dist, values='cantidad', names='tipo_pago', title="💳 Métodos de Pago", hole=0.4)
                st.plotly_chart(fig3, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Vendido", f"${df_ventas['subtotal'].sum():,.0f}")
            col2.metric("⚖️ Total Kilos", f"{df_ventas['cantidad_kg'].sum():.1f} kg")
            col3.metric("📝 N° Ventas", df_ventas.shape[0])
            
            st.subheader("📋 Detalle de Ventas")
            st.dataframe(df_ventas.sort_values('fecha', ascending=False), use_container_width=True)
        else:
            st.info("📭 No hay ventas en la última semana")
    
    # ----- TAB 4: MERMAS (solo feriante) -----
    with tab4:
        st.header("⚠️ Registro de Mermas")
        st.caption("Registra productos dañados, vencidos o perdidos.")
        
        productos = get_productos()
        
        if productos:
            opciones = {p[1]: {'id': p[0], 'precio': p[2], 'stock': p[3]} for p in productos}
            nombres = list(opciones.keys())
            
            col1, col2 = st.columns(2)
            with col1:
                producto = st.selectbox("🍎 Producto", nombres, key="select_merma")
            with col2:
                cantidad = st.number_input("⚠️ Cantidad perdida (kg)", min_value=0.1, step=0.1, format="%.1f", key="input_merma")
            
            motivo = st.selectbox("📝 Motivo", ["Producto dañado", "Producto vencido", "Producto en mal estado", "Caída/rotura", "Otro"])
            email = st.text_input("📧 Email", value="prueba@ejemplo.com", key="email_merma")
            
            if st.button("⚠️ Registrar Merma", use_container_width=True):
                if cantidad <= opciones[producto]['stock']:
                    registrar_merma(opciones[producto]['id'], cantidad, email, motivo)
                    st.success(f"✅ Merma registrada: {cantidad} kg de {producto}")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Stock insuficiente. Solo hay {opciones[producto]['stock']:.1f} kg")
        
        # Mostrar historial de mermas
        st.markdown("---")
        st.subheader("📋 Historial de Mermas")
        df_mermas = get_mermas_semanales()
        if not df_mermas.empty:
            st.dataframe(df_mermas, use_container_width=True)
        else:
            st.info("No hay mermas registradas en la última semana")
    
    # ----- TAB 5: CONFIGURACIÓN -----
    with tab5:
        st.header("⚙️ Configuración del Sistema")
        st.info("""
        **👑 Feriante - Acceso Total**
        
        - **Inventario:** Ver y gestionar productos
        - **Ventas:** Registrar ventas (también ayudantes)
        - **Reportes:** Ver estadísticas completas
        - **Mermas:** Registrar pérdidas de producto
        - **Configuración:** Control de acceso y ajustes
        
        **📌 Compartir con ayudantes:**
        Los ayudantes pueden acceder desde el mismo enlace,
        pero solo verán las opciones de ventas y reportes.
        """)

else:
    # ==================== AYUDANTE: SOLO VENTAS ====================
    st.info("👤 **Modo Ayudante** - Solo puedes registrar ventas y ver reportes básicos")
    
    # Ayudante solo tiene dos pestañas
    tab_venta, tab_reporte = st.tabs(["💰 Registrar Venta", "📊 Reporte Semanal"])
    
    # ----- REGISTRAR VENTA (Ayudante) -----
    with tab_venta:
        st.header("💰 Nueva Venta")
        productos = get_productos()
        
        if productos:
            opciones = {p[1]: {'id': p[0], 'precio': p[2], 'stock': p[3]} for p in productos}
            nombres = list(opciones.keys())
            
            col1, col2 = st.columns(2)
            with col1:
                tipo_pago = st.selectbox("💳 Tipo de pago", ["efectivo", "tarjeta"])
                producto = st.selectbox("🍎 Producto", nombres)
            with col2:
                cantidad = st.number_input("⚖️ Cantidad (kg)", min_value=0.1, step=0.1, format="%.1f", value=0.5)
                email = st.text_input("📧 Email", value="prueba@ejemplo.com")
            
            if producto:
                precio = opciones[producto]['precio']
                stock = opciones[producto]['stock']
                subtotal = cantidad * precio
                st.info(f"💰 Precio por kg: ${precio:,.0f} | 📦 Stock: {stock:.1f} kg")
                st.metric("💵 Subtotal", f"${subtotal:,.0f}")
                
                if st.button("✅ Registrar Venta", use_container_width=True):
                    if cantidad <= stock:
                        venta_id = registrar_venta(email, subtotal, tipo_pago)
                        registrar_detalle(venta_id, opciones[producto]['id'], cantidad, precio, subtotal)
                        st.success(f"✅ Venta registrada! {cantidad} kg de {producto}")
                        st.balloons()
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Stock insuficiente. Solo hay {stock:.1f} kg")
        else:
            st.info("📭 No hay productos cargados")
    
    # ----- REPORTE SEMANAL (Ayudante - sin datos de costos) -----
    with tab_reporte:
        st.header("📊 Reporte de Ventas - Última Semana")
        df_ventas = get_ventas_semanales()
        
        if not df_ventas.empty:
            ventas_dia = df_ventas.groupby('fecha')['subtotal'].sum().reset_index()
            fig = px.bar(ventas_dia, x='fecha', y='subtotal', title="💰 Ventas por Día", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            col1.metric("💰 Total Vendido", f"${df_ventas['subtotal'].sum():,.0f}")
            col2.metric("⚖️ Total Kilos", f"{df_ventas['cantidad_kg'].sum():.1f} kg")
            
            st.subheader("📋 Detalle de Ventas")
            st.dataframe(df_ventas[['fecha', 'producto', 'cantidad_kg', 'subtotal']].sort_values('fecha', ascending=False), 
                        use_container_width=True)
        else:
            st.info("📭 No hay ventas en la última semana")

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.caption("⚡ Feria de Barrio - Base de datos Neon | Streamlit")
#para ejecutar colocamos en la terminal
#streamlit run app.py
#streamlit run app.py