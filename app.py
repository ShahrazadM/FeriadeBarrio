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

# CSS personalizado - Versión completa y corregida para iPhone
st.markdown("""
<style>
    /* === FONDO GENERAL === */
    .stApp {
        background: #f0f2f6 !important;
        background-color: #f0f2f6 !important;
    }
    
    /* === TARJETAS Y CONTENEDORES === */
    .stMarkdown, div[data-testid="stVerticalBlock"] > div {
        background: transparent;
    }
    
    /* === TÍTULO DEL NEGOCIO === */
    .business-title {
        background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
        padding: 1.2rem !important;
        border-radius: 20px !important;
        color: white !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    .business-title h1 {
        font-size: 1.8rem !important;
        margin: 0 !important;
    }
    
    .business-title p {
        font-size: 0.9rem !important;
        margin-top: 0.3rem !important;
        opacity: 0.9 !important;
    }
    
    /* === TOTAL A COBRAR === */
    .total-a-cobrar {
        background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
        color: white !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    
    /* === VUELTO === */
    .vuelto-success {
        background-color: #4CAF50 !important;
        color: white !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        text-align: center !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* === BOTONES NORMALES (VERDE) === */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #45a049 !important;
        transform: scale(1.02) !important;
    }
    
    /* === BOTÓN CONFIRMAR PAGO (CELESTE) === */
    button:has(> div:contains("CONFIRMAR PAGO")),
    button:contains("CONFIRMAR PAGO") {
        background-color: #03A9F4 !important;
    }
    button:has(> div:contains("CONFIRMAR PAGO")):hover,
    button:contains("CONFIRMAR PAGO"):hover {
        background-color: #0288D1 !important;
    }
    
    /* === CARRITO CARD === */
    .cart-header {
        background: #E8F5E9 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        border: 1px solid #A5D6A7 !important;
    }
    
    /* === TEXTOS EN GENERAL === */
    h1, h2, h3, h4, p, span, div, label {
        color: #1A1A1A !important;
    }
    
    /* === INPUTS GENERALES === */
    input, textarea, .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        font-size: 1rem !important;
    }
    
    /* === CAMPO CONTRASEÑA - FONDO BLANCO OBLIGATORIO === */
    .stTextInput input[type="password"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CCCCCC !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-size: 1rem !important;
        min-height: 50px !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input[type="password"]:focus {
        border-color: #2E7D32 !important;
        outline: none !important;
        background-color: #FFFFFF !important;
    }
    
    /* Forzar fondo blanco en autocompletado de iPhone */
    .stTextInput input:-webkit-autofill,
    .stTextInput input[type="password"]:-webkit-autofill {
        background-color: #FFFFFF !important;
        -webkit-box-shadow: 0 0 0px 1000px white inset !important;
        box-shadow: 0 0 0px 1000px white inset !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* === SELECTBOX (DESPLEGABLE) - FONDO BLANCO FORZADO === */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #2E7D32 !important;
        border-radius: 12px !important;
        min-height: 52px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* === DROPDOWN (MENÚ FLOTANTE) - FONDO BLANCO === */
    div[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    
    div[role="listbox"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        padding: 10px 14px !important;
        font-size: 1rem !important;
    }
    
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    div[data-baseweb="popover"] div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* === BOTÓN INGRESAR - VERDE OSCURO === */
    .stButton button:contains("Ingresar") {
        background-color: #2E7D32 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1rem !important;
        margin-top: 8px !important;
    }
    
    .stButton button:contains("Ingresar"):hover {
        background-color: #1B5E20 !important;
    }
    
    /* === ETIQUETAS === */
    .stTextInput label, .stSelectbox label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #1A1A1A !important;
        margin-bottom: 4px !important;
    }
    
    /* === SIDEBAR (BARRA LATERAL) === */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E0E0E0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #1A1A1A !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: #4CAF50 !important;
    }
    
    /* === BARRA SUPERIOR (GITHUB/STREAMLIT) === */
    .stApp > header {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E0E0E0 !important;
    }
    
    .stApp > header * {
        color: #1A1A1A !important;
    }
    
    /* === DATAFRAME (TABLAS) === */
    .stDataFrame {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    /* === ALERTAS === */
    .stAlert {
        background-color: #FFFFFF !important;
        border-left: 4px solid #2E7D32 !important;
        border-radius: 8px !important;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: transparent !important;
        flex-wrap: wrap !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F5F5F5 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
    }
    
    /* === MEJORAS PARA MÓVIL === */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 0.9rem !important;
            padding: 0.5rem 0.8rem !important;
        }
        
        .business-title h1 {
            font-size: 1.4rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px !important;
            font-size: 0.8rem !important;
        }
        
        input, .stSelectbox div[data-baseweb="select"] {
            font-size: 0.9rem !important;
        }
        
        .stSelectbox div[data-baseweb="select"] {
            min-height: 48px !important;
        }
        
        .stTextInput input[type="password"] {
            min-height: 48px !important;
        }
    }
    
    /* === INFO Y WARNING === */
    .stInfo, .stWarning, .stError, .stSuccess {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
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
        # --- SECCIÓN PARA USUARIOS NO AUTENTICADOS ---
        st.info("👤 **Acceso para Ayudantes**")
        
        # Formulario para ayudante
        with st.form("login_ayudante_form"):
            nombre_ayudante = st.selectbox("Selecciona tu nombre", list(st.session_state.ayudantes.keys()))
            clave_ayudante = st.text_input("Contraseña", type="password")
            submitted_ayudante = st.form_submit_button("🔐 Ingresar", use_container_width=True)
            
            if submitted_ayudante:
                if autenticar_ayudante(nombre_ayudante, clave_ayudante):
                    st.success(f"✅ Bienvenido {nombre_ayudante}")
                    st.rerun()
                else:
                    st.error("❌ Nombre o contraseña incorrectos")
        
        st.markdown("---")
        st.subheader("🔐 Acceso Feriante")
        
        # Formulario para feriante (con botón)
        with st.form("login_feriante_form"):
            clave_feriante_input = st.text_input("Contraseña de dueño", type="password", key="clave_feriante_input")
            submitted_feriante = st.form_submit_button("🔐 Ingresar como Feriante", use_container_width=True)
            
            if submitted_feriante:
                if clave_feriante_input == "feriante2026":
                    st.session_state.autenticado = True
                    st.session_state.rol = "feriante"
                    st.session_state.usuario = "Feriante (Dueño)"
                    st.session_state.ayudante_autenticado = False
                    st.session_state.ayudante_actual = None
                    st.success("✅ Acceso concedido como Feriante")
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta")
        
        st.caption("Contraseña: `feriante2026`")

st.markdown("---")

# ============================================
# FUNCIONES DE BASE DE DATOS
# ============================================

@st.cache_data(ttl=5)
def get_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, feriante_email, nombre, precio_por_kilo, stock_kg FROM productos ORDER BY nombre")
    productos_raw = cur.fetchall()
    cur.close()
    conn.close()
    productos = []
    for p in productos_raw:
        productos.append((p[0], p[1], p[2], float(p[3]), float(p[4])))
    return productos

def agregar_producto(feriante_email, nombre, precio, stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO productos (feriante_email, nombre, precio_por_kilo, stock_kg)
        VALUES (%s, %s, %s, %s)
    """, (feriante_email, nombre, precio, stock))
    conn.commit()
    cur.close()
    conn.close()

def actualizar_producto(producto_id, precio, stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE productos 
        SET precio_por_kilo = %s, stock_kg = %s
        WHERE id = %s
    """, (precio, stock, producto_id))
    conn.commit()
    cur.close()
    conn.close()

def eliminar_producto(producto_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM venta_detalles WHERE producto_id = %s", (producto_id,))
    cur.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    cur.close()
    conn.close()

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

# ============================================
# FUNCIONES PARA MERMAS
# ============================================

@st.cache_data(ttl=30)
def get_resumen_mermas():
    """Obtiene el resumen de mermas por producto"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.nombre as producto,
            SUM(vd.cantidad_kg) as total_kg_perdidos,
            COUNT(vd.id) as cantidad_mermas
        FROM ventas v
        JOIN venta_detalles vd ON v.id = vd.venta_id
        JOIN productos p ON vd.producto_id = p.id
        WHERE v.tipo_pago = 'merma'
        GROUP BY p.nombre
        ORDER BY total_kg_perdidos DESC
    """)
    resumen = cur.fetchall()
    cur.close()
    conn.close()
    if resumen:
        df = pd.DataFrame(resumen, columns=['producto', 'total_kg_perdidos', 'cantidad_mermas'])
        df['total_kg_perdidos'] = df['total_kg_perdidos'].astype(float)
        return df
    return pd.DataFrame()

@st.cache_data(ttl=30)
def get_mermas_detalle():
    """Obtiene el detalle de todas las mermas"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            DATE(v.fecha) as fecha,
            p.nombre as producto,
            vd.cantidad_kg,
            v.observacion as motivo
        FROM ventas v
        JOIN venta_detalles vd ON v.id = vd.venta_id
        JOIN productos p ON vd.producto_id = p.id
        WHERE v.tipo_pago = 'merma'
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

def get_stock_actual_mermas():
    """Obtiene el stock actual de productos (para comparar con mermas)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT nombre, stock_kg FROM productos ORDER BY nombre
    """)
    stock = cur.fetchall()
    cur.close()
    conn.close()
    if stock:
        return pd.DataFrame(stock, columns=['producto', 'stock_actual_kg'])
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
# FUNCIONES DE INTERFAZ DE PAGO
# ============================================

def mostrar_seccion_pago(total, key_prefix=""):
    tipo_pago = st.radio(
        "💳 **Selecciona método de pago:**",
        ["💵 Efectivo", "💳 Tarjeta (POS Mercado Pago)"],
        key=f"{key_prefix}_tipo_pago",
        horizontal=True
    )
    
    st.markdown("---")
    
    if tipo_pago == "💵 Efectivo":
        st.subheader("💵 Pago en Efectivo")
        pago_cliente = st.number_input(
            "💰 Cliente paga con:", 
            min_value=0.0, 
            step=500.0, 
            format="%.0f",
            key=f"{key_prefix}_efectivo"
        )
        
        if pago_cliente >= total and total > 0:
            vuelto = pago_cliente - total
            st.markdown(f"<div class='vuelto-success'>💵 VUELTO: ${vuelto:,.0f}</div>", unsafe_allow_html=True)
            
            if st.button("✅ CONFIRMAR PAGO EN EFECTIVO", key=f"{key_prefix}_confirmar_efectivo", use_container_width=True):
                return "efectivo", True
        elif pago_cliente > 0 and pago_cliente < total:
            st.error(f"⚠️ Faltan ${total - pago_cliente:,.0f}")
        
        return None, False
    
    else:
        st.subheader("💳 Pago con Tarjeta")
        st.info("📱 El cliente pagará con el POS de Mercado Pago")
        st.caption("Una vez que el POS confirme el pago, presiona el botón para registrar la venta")
        
        if st.button("✅ CONFIRMAR PAGO CON TARJETA", key=f"{key_prefix}_confirmar_tarjeta", use_container_width=True):
            return "tarjeta", True
        
        return None, False

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
# INTERFAZ PRINCIPAL - FERIANTE
# ============================================

if st.session_state.rol == "feriante":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📦 Inventario", "➕ Agregar Producto", "🛒 Venta", "📊 Reportes", "⚠️ Mermas"])
    
        # ----- TAB 1: VER INVENTARIO Y EDITAR -----
    # ----- TAB 2: AGREGAR NUEVO PRODUCTO -----
    # ----- TAB 1: VER INVENTARIO Y EDITAR -----
    # ----- TAB 1: VER INVENTARIO Y EDITAR -----
    with tab1:
        st.header("📦 Inventario Actual")
        productos = get_productos()
        
        if productos:
            st.subheader("📋 Lista de Productos")
            
            # Cabeceras de la tabla
            col1, col2, col3, col4, col5 = st.columns([2, 1.2, 1.2, 0.6, 0.6])
            with col1:
                st.markdown("**🍎 Producto**")
            with col2:
                st.markdown("**💰 Precio por kg**")
            with col3:
                st.markdown("**📦 Stock (kg)**")
            with col4:
                st.markdown("**💾**")
            with col5:
                st.markdown("**🗑️**")
            st.markdown("---")
            
            for p in productos:
                # Asegurar que los valores sean float
                precio_actual = float(p[3])
                stock_actual = float(p[4])
                
                col1, col2, col3, col4, col5 = st.columns([2, 1.2, 1.2, 0.6, 0.6])
                with col1:
                    st.markdown(f"**{p[2]}**")
                with col2:
                    nuevo_precio = st.number_input(
                        "Precio", 
                        value=precio_actual,  # ← AHORA ES FLOAT
                        step=100.0, 
                        format="%.0f",
                        key=f"precio_{p[0]}",
                        label_visibility="collapsed",
                        help="Precio por kilogramo"
                    )
                with col3:
                    nuevo_stock = st.number_input(
                        "Stock", 
                        value=stock_actual,  # ← AHORA ES FLOAT
                        step=5.0, 
                        format="%.1f",
                        key=f"stock_{p[0]}",
                        label_visibility="collapsed",
                        help="Cantidad disponible en kilogramos"
                    )
                with col4:
                    if st.button(f"💾", key=f"save_{p[0]}", help="Guardar cambios"):
                        if nuevo_precio != precio_actual or nuevo_stock != stock_actual:
                            actualizar_producto(p[0], nuevo_precio, nuevo_stock)
                            st.success(f"✅ {p[2]} actualizado")
                            st.cache_data.clear()
                            time.sleep(0.5)
                            st.rerun()
                with col5:
                    if st.button(f"🗑️", key=f"del_{p[0]}", help="Eliminar producto"):
                        eliminar_producto(p[0])
                        st.success(f"❌ {p[2]} eliminado")
                        st.cache_data.clear()
                        time.sleep(0.5)
                        st.rerun()
                st.markdown("---")
            
            # Mostrar productos con stock bajo
            stock_bajo = [p for p in productos if float(p[4]) < 10]
            if stock_bajo:
                st.warning("⚠️ **Productos con stock bajo (< 10 kg):**")
                for p in stock_bajo:
                    st.write(f"- **{p[2]}**: {float(p[4]):.1f} kg disponibles")
        else:
            st.info("📭 No hay productos cargados. Ve a la pestaña 'Agregar Producto' para comenzar.")


    # ----- TAB 2: AGREGAR NUEVO PRODUCTO -----

    # ----- TAB 2: AGREGAR NUEVO PRODUCTO -----
    with tab2:
        st.header("➕ Agregar Nuevo Producto")
        
        with st.form("nuevo_producto_form"):
            col1, col2 = st.columns(2)
            with col1:
                nombre_producto = st.text_input(
                    "🍎 **Nombre del producto**", 
                    placeholder="Ej: Plátanos, Paltas, Naranjas",
                    help="Ejemplo: Manzanas, Tomates, Papas"
                )
            with col2:
                precio_texto = st.text_input(
                    "💰 **Precio por kilo ($)**", 
                    placeholder="Ej: 1200  o  1.200  o  1,200",
                    help="Escribe : 1200, 1.200 o 1,200 ",
                    value="1000"
                )
                
                # Función para formatear y mostrar el precio ingresado
                def mostrar_precio_formateado(texto):
                    try:
                        # Limpiar caracteres no numéricos (excepto el punto y coma que usamos para separar miles)
                        limpio = texto.replace(".", "").replace(",", "").strip()
                        if limpio.isdigit():
                            valor = int(limpio)
                            # Formato chileno: 1.200
                            return f"💰 Convertido a: ${valor:,.0f}".replace(",", ".")
                    except:
                        pass
                    return "⚠️ Formato inválido"
                
                if precio_texto:
                    st.caption(mostrar_precio_formateado(precio_texto))
            
            stock_inicial = st.number_input(
                "📦 **Stock inicial (kg)**", 
                min_value=0.0, 
                step=5.0, 
                format="%.1f", 
                value=10.0,
                help="Cantidad inicial en kilos (ej: 10.5 = 10,5 kg)"
            )
            email_feriante = st.text_input("📧 **Email del feriante**", value="prueba@ejemplo.com")
            
            submitted = st.form_submit_button("➕ Agregar Producto", use_container_width=True)
            
            if submitted:
                errores = []
                
                if not nombre_producto:
                    errores.append("El nombre del producto es obligatorio")
                
                # Procesar precio
                try:
                    precio_limpio = precio_texto.replace(".", "").replace(",", "").strip()
                    if not precio_limpio.isdigit():
                        errores.append("El precio debe ser un número (ej: 1200, 1.200 o 1,200)")
                    else:
                        precio_producto = float(precio_limpio)
                        if precio_producto < 100:
                            errores.append(f"El precio debe ser mayor o igual a 100. Ingresaste: {precio_producto:,.0f}".replace(",", "."))
                except:
                    errores.append("El precio no es válido")
                
                if errores:
                    for error in errores:
                        st.error(f"❌ {error}")
                else:
                    agregar_producto(email_feriante, nombre_producto, precio_producto, stock_inicial)
                    st.success(f"✅ Producto '{nombre_producto}' agregado correctamente")
                    st.info(f"💰 Precio guardado: ${precio_producto:,.0f}".replace(",", "."))
                    st.cache_data.clear()
                    time.sleep(2)
                    st.rerun()
     # ----- TAB 3: VENTA (carrito) -----
    with tab3:
        st.header("🛒 Carrito de Compras")
        productos = get_productos()
        
        if productos:
            opciones = {p[2]: {'id': p[0], 'precio': p[3], 'stock': p[4]} for p in productos}
            nombres = list(opciones.keys())
            
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
            
            if st.session_state.carrito:
                st.subheader("🛍️ Carrito actual")
                for idx, item in enumerate(st.session_state.carrito):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                    with col1:
                        st.write(f"**{item['nombre']}**")
                    with col2:
                        st.write(f"{item['cantidad']:.1f} kg")
                    with col3:
                        st.write(f"${item['subtotal']:,.0f}")
                    with col4:
                        if st.button("🗑️", key=f"del_fer_{idx}"):
                            eliminar_del_carrito(idx)
                            st.rerun()
                
                total = calcular_total_carrito()
                
                st.markdown(f"""
                <div class="total-a-cobrar">
                    <h2>💰 TOTAL A COBRAR: ${total:,.0f}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                tipo_pago, confirmado = mostrar_seccion_pago(total, "feriante")
                
                if confirmado:
                    registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, tipo_pago, total)
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
        else:
            st.info("📭 No hay productos cargados")
    
    # ----- TAB 4: REPORTES -----
    with tab4:
        st.header("📊 Reporte Semanal de Ventas")
        df = get_ventas_semanales()
        if not df.empty:
            ventas_dia = df.groupby('fecha')['subtotal'].sum().reset_index()
            fig = px.bar(ventas_dia, x='fecha', y='subtotal', title="Ventas por Día", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
            top = df.groupby('producto')['cantidad_kg'].sum().reset_index().sort_values('cantidad_kg', ascending=False).head(5)
            fig2 = px.bar(top, x='producto', y='cantidad_kg', title="Top 5 Productos más Vendidos")
            st.plotly_chart(fig2, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Vendido", f"${df['subtotal'].sum():,.0f}")
            col2.metric("⚖️ Total Kilos Vendidos", f"{df['cantidad_kg'].sum():.1f} kg")
            col3.metric("📝 N° Ventas", df.shape[0])
            
            st.subheader("📋 Detalle de Ventas")
            st.dataframe(df.sort_values('fecha', ascending=False), use_container_width=True)
        else:
            st.info("📭 No hay ventas en la última semana")
    
    # ----- TAB 5: MERMAS (con resumen y detalle) -----
    with tab5:
        st.header("⚠️ Registrar Nueva Merma")
        
        productos = get_productos()
        if productos:
            opciones = {p[2]: {'id': p[0], 'stock': p[4]} for p in productos}
            
            col1, col2 = st.columns(2)
            with col1:
                producto_merma = st.selectbox("🍎 Producto", list(opciones.keys()), key="prod_merma")
            with col2:
                cantidad_merma = st.number_input("⚠️ Cantidad perdida (kg)", min_value=0.1, step=0.5, format="%.1f", key="cant_merma")
            
            motivo = st.selectbox("📝 Motivo", ["Producto dañado", "Producto vencido", "Producto en mal estado", "Caída/rotura", "Otro"])
            
            if st.button("⚠️ Registrar Merma", use_container_width=True):
                if cantidad_merma <= opciones[producto_merma]['stock']:
                    registrar_merma(opciones[producto_merma]['id'], cantidad_merma, "prueba@ejemplo.com", motivo)
                    st.success(f"✅ Merma registrada: {cantidad_merma} kg de {producto_merma}")
                    st.cache_data.clear()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Stock insuficiente. Solo hay {opciones[producto_merma]['stock']:.1f} kg")
        
        st.markdown("---")
        
        # ========== RESUMEN DE MERMAS ==========
        st.header("📊 Resumen de Mermas por Producto")
        
        df_resumen = get_resumen_mermas()
        if not df_resumen.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📋 Tabla Resumen")
                st.dataframe(df_resumen, use_container_width=True)
            
            with col2:
                # Gráfico de mermas por producto
                fig_mermas = px.bar(
                    df_resumen, 
                    x='producto', 
                    y='total_kg_perdidos',
                    title="Kilos Perdidos por Producto",
                    labels={'producto': 'Producto', 'total_kg_perdidos': 'Kilos perdidos'},
                    color='total_kg_perdidos',
                    text_auto=True
                )
                st.plotly_chart(fig_mermas, use_container_width=True)
            
            # Métricas totales
            total_kg_perdidos = df_resumen['total_kg_perdidos'].sum()
            total_mermas = df_resumen['cantidad_mermas'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📦 Total Kilos Perdidos", f"{total_kg_perdidos:.1f} kg")
            col2.metric("📝 Total de Mermas", total_mermas)
            col3.metric("🥇 Producto más afectado", df_resumen.iloc[0]['producto'] if not df_resumen.empty else "Ninguno")
        else:
            st.info("📭 No hay mermas registradas")
        
        st.markdown("---")
        
        # ========== DETALLE DE MERMAS ==========
        st.header("📋 Historial Detallado de Mermas")
        
        df_detalle = get_mermas_detalle()
        if not df_detalle.empty:
            # Selector de filtro por producto
            productos_merma = ["Todos"] + sorted(df_detalle['producto'].unique().tolist())
            filtro_producto = st.selectbox("🔍 Filtrar por producto", productos_merma)
            
            if filtro_producto != "Todos":
                df_detalle = df_detalle[df_detalle['producto'] == filtro_producto]
            
            st.dataframe(df_detalle, use_container_width=True)
            
            # Exportar a CSV
            csv = df_detalle.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar historial de mermas (CSV)",
                data=csv,
                file_name="historial_mermas.csv",
                mime="text/csv",
            )
        else:
            st.info("📭 No hay mermas registradas en el historial")
        
        # ========== COMPARATIVA STOCK ACTUAL VS MERMAS ==========
        st.markdown("---")
        st.header("📊 Comparativa: Stock Actual vs Mermas")
        
        df_stock = get_stock_actual_mermas()
        if not df_resumen.empty and not df_stock.empty:
            comparativa = pd.merge(df_stock, df_resumen, on='producto', how='left')
            comparativa = comparativa.fillna(0)
            comparativa.rename(columns={'stock_actual_kg': 'Stock Actual (kg)', 'total_kg_perdidos': 'Kilos Perdidos por Mermas'}, inplace=True)
            comparativa['Stock Actual (kg)'] = comparativa['Stock Actual (kg)'].round(1)
            comparativa['Kilos Perdidos por Mermas'] = comparativa['Kilos Perdidos por Mermas'].round(1)
            comparativa = comparativa.sort_values('Kilos Perdidos por Mermas', ascending=False)
            
            st.dataframe(comparativa, use_container_width=True)
        else:
            st.info("📭 No hay datos suficientes para la comparativa")

# ============================================
# INTERFAZ - AYUDANTE
# ============================================

elif st.session_state.rol == "ayudante":
    st.header("🛒 Carrito de Compras")
    productos = get_productos()
    
    if productos:
        opciones = {p[2]: {'id': p[0], 'precio': p[3], 'stock': p[4]} for p in productos}
        nombres = list(opciones.keys())
        
        col1, col2 = st.columns([2, 1])
        with col1:
            producto = st.selectbox("🍎 Producto", nombres, key="prod_ayudante")
        with col2:
            cantidad = st.number_input("⚖️ kg", min_value=0.1, step=0.1, format="%.1f", key="cant_ayudante")
        
        if producto:
            precio = opciones[producto]['precio']
            stock = opciones[producto]['stock']
            st.info(f"💰 ${precio:,.0f}/kg | 📦 Stock: {stock:.1f} kg")
            if st.button("➕ Agregar", key="agregar_ayudante"):
                agregar_al_carrito(opciones[producto]['id'], producto, cantidad, precio, stock)
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.carrito:
            st.subheader("🛍️ Carrito actual")
            for idx, item in enumerate(st.session_state.carrito):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
                with col1:
                    st.write(f"**{item['nombre']}**")
                with col2:
                    st.write(f"{item['cantidad']:.1f} kg")
                with col3:
                    st.write(f"${item['subtotal']:,.0f}")
                with col4:
                    if st.button("🗑️", key=f"del_ayu_{idx}"):
                        eliminar_del_carrito(idx)
                        st.rerun()
            
            total = calcular_total_carrito()
            st.markdown(f"""
            <div class="total-a-cobrar">
                <h2>💰 TOTAL A COBRAR: ${total:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            tipo_pago, confirmado = mostrar_seccion_pago(total, "ayudante")
            
            if confirmado:
                registrar_venta_completa("prueba@ejemplo.com", st.session_state.carrito, tipo_pago, total)
                st.success(f"✅ ¡Venta confirmada! Total: ${total:,.0f}")
                st.session_state.carrito = []
                st.balloons()
                st.cache_data.clear()
                time.sleep(1)
                st.rerun()
            
            if st.button("🗑️ Vaciar Carrito", key="vaciar_ayudante"):
                limpiar_carrito()
                st.rerun()
        else:
            st.info("🛒 El carrito está vacío")
    else:
        st.info("📭 No hay productos cargados")

# ============================================
# INTERFAZ - INVITADO
# ============================================

else:
    st.warning("👤 **Modo Invitado** - Sin autenticación")
    st.info("Para usar el carrito de compras múltiple, ingresa como Ayudante o Feriante")
    
    productos = get_productos()
    if productos:
        opciones = {p[2]: {'precio': p[3], 'stock': p[4]} for p in productos}
        col1, col2 = st.columns(2)
        with col1:
            producto = st.selectbox("Producto", list(opciones.keys()))
        with col2:
            cantidad = st.number_input("kg", min_value=0.1, step=0.1)
        
        if producto:
            subtotal = cantidad * opciones[producto]['precio']
            st.metric("Total", f"${subtotal:,.0f}")
            if st.button("Registrar venta (Demo)"):
                st.info("Demo - Registro simulado")

st.markdown("---")
st.caption(f"🛒 {st.session_state.negocio_nombre} - Frescura como nunca | Powered by Streamlit")

#para ejecutar colocamos en la terminal
#streamlit run app.py
#streamlit run app.py