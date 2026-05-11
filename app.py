import streamlit as st
import pandas as pd
import plotly.express as px
import time
from db_config import get_connection
import hashlib

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(page_title="Frutería San Sebastián", page_icon="🛒", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #45a049 !important;
        transform: scale(1.02) !important;
        box-shadow: 0 4px 12px rgba(76,175,80,0.3) !important;
    }
    
    .business-title {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .cart-header {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #a5d6a7;
    }
    
    .vuelto-success {
        background-color: #4CAF50;
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .total-a-cobrar {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .total-a-cobrar h2 {
        margin: 0;
        font-size: 2rem;
    }
    
    .product-card {
        background-color: white;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HASH PARA CONTRASEÑAS
# ============================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# ============================================
# GESTIÓN DE AYUDANTES
# ============================================

if 'ayudantes' not in st.session_state:
    st.session_state.ayudantes = {
        "Pedro": {"clave_hash": hash_password("pedro2026"), "activo": True},
        "Maria": {"clave_hash": hash_password("maria2026"), "activo": True},
        "Jose": {"clave_hash": hash_password("jose2026"), "activo": True}
    }
if 'ayudante_actual' not in st.session_state:
    st.session_state.ayudante_actual = None
if 'ayudante_autenticado' not in st.session_state:
    st.session_state.ayudante_autenticado = False

def autenticar_ayudante(nombre, clave):
    if nombre in st.session_state.ayudantes:
        ayudante = st.session_state.ayudantes[nombre]
        if ayudante['activo'] and verify_password(clave, ayudante['clave_hash']):
            st.session_state.ayudante_actual = nombre
            st.session_state.ayudante_autenticado = True
            st.session_state.rol = "ayudante"
            st.session_state.usuario = f"Ayudante: {nombre}"
            return True
    return False

def logout_ayudante():
    st.session_state.ayudante_actual = None
    st.session_state.ayudante_autenticado = False
    st.session_state.rol = "ayudante_no_auth"
    st.session_state.usuario = "Sin autenticar"

def agregar_ayudante(nombre, clave):
    if nombre in st.session_state.ayudantes:
        return False, "El ayudante ya existe"
    if len(st.session_state.ayudantes) >= 3:
        return False, "Máximo 3 ayudantes permitidos"
    st.session_state.ayudantes[nombre] = {
        'clave_hash': hash_password(clave),
        'activo': True
    }
    return True, "Ayudante agregado correctamente"

def eliminar_ayudante(nombre):
    if nombre in st.session_state.ayudantes:
        del st.session_state.ayudantes[nombre]
        return True
    return False

# ============================================
# SISTEMA DE ROLES
# ============================================

if 'rol' not in st.session_state:
    st.session_state.rol = "ayudante_no_auth"
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = "Sin autenticar"
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'negocio_nombre' not in st.session_state:
    st.session_state.negocio_nombre = "Frutería San Sebastián"

def autenticar_feriante():
    if st.session_state.clave_feriante == "feriante2026":
        st.session_state.autenticado = True
        st.session_state.rol = "feriante"
        st.session_state.usuario = "Feriante (Dueño)"
        st.session_state.ayudante_autenticado = False
        st.session_state.ayudante_actual = None
    else:
        st.error("❌ Contraseña incorrecta")

def cambiar_a_modo_ayudante():
    st.session_state.autenticado = False
    st.session_state.rol = "ayudante_no_auth"
    st.session_state.usuario = "Sin autenticar"
    st.session_state.ayudante_autenticado = False
    st.session_state.ayudante_actual = None

# ============================================
# BARRA LATERAL
# ============================================

with st.sidebar:
    st.header("👤 Control de Acceso")
    
    if st.session_state.rol == "feriante":
        st.success(f"✅ **{st.session_state.usuario}**")
        
        st.markdown("---")
        st.subheader("🏪 Configurar Negocio")
        nuevo_nombre = st.text_input("Nombre del local", value=st.session_state.negocio_nombre)
        if nuevo_nombre != st.session_state.negocio_nombre:
            st.session_state.negocio_nombre = nuevo_nombre
            st.rerun()
        
        st.markdown("---")
        st.subheader("👥 Gestión de Ayudantes (máx 3)")
        
        for nombre, data in st.session_state.ayudantes.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{nombre}**")
            with col2:
                if st.button(f"🗑️", key=f"del_{nombre}"):
                    if eliminar_ayudante(nombre):
                        st.success(f"Eliminado: {nombre}")
                        st.rerun()
        
        with st.expander("➕ Agregar Ayudante"):
            nuevo_ayudante = st.text_input("Nombre")
            nueva_clave = st.text_input("Contraseña", type="password")
            if st.button("Registrar"):
                if nuevo_ayudante and nueva_clave:
                    ok, msg = agregar_ayudante(nuevo_ayudante, nueva_clave)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        
        st.markdown("---")
        if st.button("🔓 Cambiar a Modo Ayudante", use_container_width=True):
            cambiar_a_modo_ayudante()
            st.rerun()
    
    elif st.session_state.rol == "ayudante":
        st.success(f"✅ **{st.session_state.usuario}**")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            logout_ayudante()
            st.rerun()
    
    else:
        st.info("👤 **Acceso para Ayudantes**")
        
        with st.form("login_ayudante_form"):
            nombre_ayudante = st.selectbox("Selecciona tu nombre", list(st.session_state.ayudantes.keys()))
            clave_ayudante = st.text_input("Contraseña", type="password")
            if st.form_submit_button("🔐 Ingresar", use_container_width=True):
                if autenticar_ayudante(nombre_ayudante, clave_ayudante):
                    st.success(f"✅ Bienvenido {nombre_ayudante}")
                    st.rerun()
                else:
                    st.error("❌ Nombre o contraseña incorrectos")
        
        st.markdown("---")
        st.subheader("🔐 Acceso Feriante")
        st.text_input("Contraseña de dueño", type="password", key="clave_feriante", on_change=autenticar_feriante)
        st.caption("Contraseña: `feriante2026`")

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

def registrar_venta_completa(feriante_email, items_carrito, tipo_pago, total):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ventas (feriante_email, total, tipo_pago)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (feriante_email, total, tipo_pago))
    venta_id = cur.fetchone()[0]
    for item in items_carrito:
        cur.execute("""
            INSERT INTO venta_detalles (venta_id, producto_id, cantidad_kg, precio_por_kilo, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (venta_id, item['producto_id'], item['cantidad'], item['precio'], item['subtotal']))
    conn.commit()
    cur.close()
    conn.close()
    return venta_id

def registrar_merma(producto_id, cantidad_kg, email, motivo):
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
# FUNCIONES DEL CARRITO
# ============================================

def agregar_al_carrito(producto_id, nombre, cantidad, precio, stock):
    if cantidad <= 0:
        st.warning("⚠️ La cantidad debe ser mayor a 0")
        return False
    if cantidad > stock:
        st.warning(f"⚠️ Stock insuficiente. Solo hay {stock:.1f} kg")
        return False
    for item in st.session_state.carrito:
        if item['producto_id'] == producto_id:
            nueva_cantidad = item['cantidad'] + cantidad
            if nueva_cantidad > stock:
                st.warning(f"⚠️ No puedes agregar más. Stock disponible: {stock:.1f} kg")
                return False
            item['cantidad'] = nueva_cantidad
            item['subtotal'] = nueva_cantidad * item['precio']
            st.success(f"✅ Actualizado: {nombre} ahora {nueva_cantidad:.1f} kg")
            return True
    st.session_state.carrito.append({
        'producto_id': producto_id, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio, 'subtotal': cantidad * precio
    })
    st.success(f"✅ Agregado: {cantidad:.1f} kg de {nombre}")
    return True

def eliminar_del_carrito(idx):
    producto_eliminado = st.session_state.carrito[idx]['nombre']
    del st.session_state.carrito[idx]
    st.success(f"❌ Eliminado: {producto_eliminado}")

def limpiar_carrito():
    st.session_state.carrito = []
    st.success("🛒 Carrito vacío")

def calcular_total_carrito():
    return sum(item['subtotal'] for item in st.session_state.carrito)

# ============================================
# TÍTULO
# ============================================

st.markdown(f"""
<div class="business-title">
    <h1>🛒 {st.session_state.negocio_nombre}</h1>
    <p>🌿 Frutas y Verduras Frescas - Calidad y Confianza 🌿</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# INTERFAZ
# ============================================

if st.session_state.rol == "feriante":
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Inventario", "🛒 Venta", "📊 Reportes", "⚠️ Mermas"])
    
    with tab1:
        st.header("📦 Inventario Actual")
        productos = get_productos()
        if productos:
            df = pd.DataFrame(productos, columns=['id', 'nombre', 'precio_por_kilo', 'stock_kg'])
            df['precio_por_kilo'] = df['precio_por_kilo'].apply(lambda x: f"${x:,.0f}/kg")
            df['stock_kg'] = df['stock_kg'].apply(lambda x: f"{x:.1f} kg")
            st.dataframe(df[['nombre', 'precio_por_kilo', 'stock_kg']], use_container_width=True)
            stock_bajo = [p for p in productos if p[3] < 10]
            if stock_bajo:
                st.warning("⚠️ **Productos con stock bajo (< 10 kg):**")
                for p in stock_bajo:
                    st.write(f"- {p[1]}: {p[3]:.1f} kg")
    
    with tab2:
        st.header("🛒 Carrito de Compras")
        productos = get_productos()
        if productos:
            opciones = {p[1]: {'id': p[0], 'precio': p[2], 'stock': p[3]} for p in productos}
            nombres = list(opciones.keys())
            
            # Selección de productos
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    producto = st.selectbox("🍎 Producto", nombres, key="prod_feriante")
                with col2:
                    cantidad = st.number_input("⚖️ kg", min_value=0.1, step=0.1, format="%.1f", key="cant_feriante")
                
                if producto:
                    precio = opciones[producto]['precio']
                    stock = opciones[producto]['stock']
                    st.info(f"💰 ${precio:,.0f}/kg | 📦 Stock: {stock:.1f} kg")
                    if st.button("➕ Agregar", key="agregar_feriante"):
                        agregar_al_carrito(opciones[producto]['id'], producto, cantidad, precio, stock)
                        st.rerun()
            
            st.markdown("---")
            
            # Carrito
            if st.session_state.carrito:
                st.subheader("🛍️ Productos en el carrito")
                for idx, item in enumerate(st.session_state.carrito):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                    with col1:
                        st.write(f"**{item['nombre']}**")
                    with col2:
                        st.write(f"{item['cantidad']:.1f} kg")
                    with col3:
                        st.write(f"${item['subtotal']:,.0f}")
                    with col4:
                        if st.button("🗑️", key=f"del_{idx}"):
                            eliminar_del_carrito(idx)
                            st.rerun()
                
                st.markdown("---")
                total = calcular_total_carrito()
                
                # Total a cobrar (visible siempre)
                st.markdown(f"""
                <div class="total-a-cobrar">
                    <h2>💰 TOTAL A COBRAR: ${total:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Tipo de pago y vuelto
                col_efectivo, col_tarjeta = st.columns(2)
                
                with col_efectivo:
                    st.subheader("💵 Efectivo")
                    pago_cliente = st.number_input("Cliente paga con:", min_value=0.0, step=1000.0, format="%.0f", key="pago_efectivo")
                    
                    if pago_cliente >= total and total > 0:
                        vuelto = pago_cliente - total
                        st.markdown(f"<div class='vuelto-success'>💵 VUELTO: ${vuelto:,.0f}</div>", unsafe_allow_html=True)
                        confirmar = st.button("✅ CONFIRMAR PAGO EN EFECTIVO", key="confirmar_efectivo", use_container_width=True)
                        if confirmar:
                            registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, "efectivo", total)
                            st.success(f"✅ ¡Venta confirmada! Total: ${total:,.0f}")
                            st.session_state.carrito = []
                            st.balloons()
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
                    elif pago_cliente > 0 and pago_cliente < total:
                        st.error(f"⚠️ Faltan ${total - pago_cliente:,.0f}")
                
                with col_tarjeta:
                    st.subheader("💳 Tarjeta")
                    if st.button("✅ CONFIRMAR PAGO CON TARJETA", key="confirmar_tarjeta", use_container_width=True):
                        registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, "tarjeta", total)
                        st.success(f"✅ ¡Venta confirmada! Total: ${total:,.0f}")
                        st.session_state.carrito = []
                        st.balloons()
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
                
                if st.button("🗑️ Vaciar Carrito", key="vaciar_feriante"):
                    limpiar_carrito()
                    st.rerun()
            else:
                st.info("🛒 El carrito está vacío. Agrega productos para comenzar.")
    
    with tab3:
        st.header("📊 Reporte Semanal")
        df = get_ventas_semanales()
        if not df.empty:
            ventas_dia = df.groupby('fecha')['subtotal'].sum().reset_index()
            fig = px.bar(ventas_dia, x='fecha', y='subtotal', title="Ventas por Día", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            top = df.groupby('producto')['cantidad_kg'].sum().reset_index().sort_values('cantidad_kg', ascending=False).head(5)
            fig2 = px.bar(top, x='producto', y='cantidad_kg', title="Top 5 Productos")
            st.plotly_chart(fig2, use_container_width=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Vendido", f"${df['subtotal'].sum():,.0f}")
            c2.metric("Total Kilos", f"{df['cantidad_kg'].sum():.1f} kg")
            c3.metric("N° Ventas", df.shape[0])
            st.dataframe(df.sort_values('fecha', ascending=False), use_container_width=True)
    
    with tab4:
        st.header("⚠️ Mermas")
        productos = get_productos()
        if productos:
            opciones = {p[1]: {'id': p[0], 'stock': p[3]} for p in productos}
            col1, col2 = st.columns(2)
            with col1:
                prod = st.selectbox("Producto", list(opciones.keys()))
            with col2:
                cant = st.number_input("kg perdidos", min_value=0.1, step=0.1)
            motivo = st.selectbox("Motivo", ["Dañado", "Vencido", "Mal estado", "Caída", "Otro"])
            if st.button("Registrar Merma"):
                if cant <= opciones[prod]['stock']:
                    registrar_merma(opciones[prod]['id'], cant, "prueba@ejemplo.com", motivo)
                    st.success(f"Merma registrada: {cant} kg de {prod}")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()

elif st.session_state.rol == "ayudante":
    # Ayudante autenticado - misma interfaz de ventas
    st.header("🛒 Carrito de Compras")
    productos = get_productos()
    if productos:
        opciones = {p[1]: {'id': p[0], 'precio': p[2], 'stock': p[3]} for p in productos}
        nombres = list(opciones.keys())
        
        col1, col2 = st.columns([2, 1])
        with col1:
            producto = st.selectbox("🍎 Producto", nombres)
        with col2:
            cantidad = st.number_input("⚖️ kg", min_value=0.1, step=0.1, format="%.1f")
        
        if producto:
            precio = opciones[producto]['precio']
            stock = opciones[producto]['stock']
            st.info(f"💰 ${precio:,.0f}/kg | 📦 Stock: {stock:.1f} kg")
            if st.button("➕ Agregar"):
                agregar_al_carrito(opciones[producto]['id'], producto, cantidad, precio, stock)
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.carrito:
            st.subheader("🛍️ Carrito actual")
            for idx, item in enumerate(st.session_state.carrito):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                col1.write(f"**{item['nombre']}**")
                col2.write(f"{item['cantidad']:.1f} kg")
                col3.write(f"${item['subtotal']:,.0f}")
                if col4.button("🗑️", key=f"del_{idx}"):
                    eliminar_del_carrito(idx)
                    st.rerun()
            
            total = calcular_total_carrito()
            st.markdown(f"<div class='total-a-cobrar'><h2>💰 TOTAL A COBRAR: ${total:,.0f}</h2></div>", unsafe_allow_html=True)
            
            col_efectivo, col_tarjeta = st.columns(2)
            with col_efectivo:
                pago = st.number_input("Cliente paga:", min_value=0.0, step=1000.0)
                if pago >= total and total > 0:
                    st.markdown(f"<div class='vuelto-success'>💵 VUELTO: ${pago - total:,.0f}</div>", unsafe_allow_html=True)
                    if st.button("✅ CONFIRMAR PAGO EN EFECTIVO", use_container_width=True):
                        registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, "efectivo", total)
                        st.success(f"✅ Venta confirmada! Total: ${total:,.0f}")
                        st.session_state.carrito = []
                        st.balloons()
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
            with col_tarjeta:
                if st.button("✅ CONFIRMAR PAGO CON TARJETA", use_container_width=True):
                    registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, "tarjeta", total)
                    st.success(f"✅ Venta confirmada! Total: ${total:,.0f}")
                    st.session_state.carrito = []
                    st.balloons()
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
            
            if st.button("🗑️ Vaciar Carrito"):
                limpiar_carrito()
                st.rerun()
        else:
            st.info("🛒 Carrito vacío")

else:
    # Invitado (no autenticado) - solo venta simple (sin carrito)
    st.warning("👤 Modo invitado: sin autenticación")
    st.info("Para usar el carrito múltiple, ingresa como Ayudante o Feriante")
    
    productos = get_productos()
    if productos:
        opciones = {p[1]: {'precio': p[2], 'stock': p[3]} for p in productos}
        col1, col2 = st.columns(2)
        with col1:
            producto = st.selectbox("Producto", list(opciones.keys()))
        with col2:
            cantidad = st.number_input("kg", min_value=0.1, step=0.1)
        
        if producto:
            precio = opciones[producto]['precio']
            subtotal = cantidad * precio
            st.metric("Total", f"${subtotal:,.0f}")
            if st.button("Registrar venta"):
                # Registro directo
                st.info("Registrado (demo)")

st.markdown("---")
st.caption(f"🛒 {st.session_state.negocio_nombre} - Sierra como nunca | Powered by Streamlit")

#para ejecutar colocamos en la terminal
#streamlit run app.py
#streamlit run app.py