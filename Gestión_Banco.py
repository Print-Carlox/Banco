import streamlit as st
from datetime import datetime

# -------------------------------
# Clase CuentaCorriente
# -------------------------------
class CuentaCorriente:
    def __init__(self, numero_cuenta: str, saldo_inicial: float):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.depositos_del_dia = 0
        self.retiros_del_dia = 0

    def deposito(self, monto: float):
        self.saldo += monto
        self.depositos_del_dia += monto
        return f"Depósito de {monto:.2f} realizado en cuenta {self.numero_cuenta}. Nuevo saldo: {self.saldo:.2f}"

    def retiro(self, monto: float):
        if monto <= self.saldo:
            self.saldo -= monto
            self.retiros_del_dia += monto
            return f"Retiro de {monto:.2f} realizado en cuenta {self.numero_cuenta}. Nuevo saldo: {self.saldo:.2f}"
        else:
            return f"Fondos insuficientes en cuenta {self.numero_cuenta}. Saldo actual: {self.saldo:.2f}"

# -------------------------------
# Funciones de archivo
# -------------------------------
def cargar_cuentas(nombre_archivo="cuentas.txt"):
    cuentas = []
    try:
        with open(nombre_archivo, "r") as f:
            for linea in f:
                numero, saldo = linea.strip().split(",")
                cuentas.append(CuentaCorriente(numero, float(saldo)))
    except FileNotFoundError:
        pass
    return cuentas

def guardar_cuentas(cuentas, nombre_archivo="cuentas.txt"):
    with open(nombre_archivo, "w") as f:
        for cuenta in cuentas:
            f.write(f"{cuenta.numero_cuenta},{cuenta.saldo}\n")

# -------------------------------
# Streamlit App
# -------------------------------
st.title("🏦 Banco - Gestión de Cuentas Corrientes")

# Estado persistente en la sesión
if "cuentas" not in st.session_state:
    st.session_state.cuentas = cargar_cuentas()

# Selección de cuenta
cuentas = st.session_state.cuentas
opciones = [c.numero_cuenta for c in cuentas]
cuenta_seleccionada = st.selectbox("Seleccione una cuenta:", opciones)

cuenta = next((c for c in cuentas if c.numero_cuenta == cuenta_seleccionada), None)

st.write(f"**Saldo actual:** {cuenta.saldo:.2f}")

# Operaciones
st.subheader("Operaciones")
monto = st.number_input("Monto", min_value=0.0, step=10.0)

col1, col2 = st.columns(2)
with col1:
    if st.button("Depositar"):
        resultado = cuenta.deposito(monto)
        st.success(resultado)
with col2:
    if st.button("Retirar"):
        resultado = cuenta.retiro(monto)
        if "Fondos insuficientes" in resultado:
            st.error(resultado)
        else:
            st.success(resultado)

# Crear nueva cuenta
st.subheader("Crear nueva cuenta")
nuevo_numero = st.text_input("Número de cuenta")
saldo_inicial = st.number_input("Saldo inicial", min_value=0.0, step=100.0)
if st.button("Crear cuenta"):
    if nuevo_numero and not any(c.numero_cuenta == nuevo_numero for c in cuentas):
        cuentas.append(CuentaCorriente(nuevo_numero, saldo_inicial))
        st.success(f"Cuenta {nuevo_numero} creada con saldo {saldo_inicial:.2f}")
    else:
        st.error("Número de cuenta inválido o ya existente.")

# Eliminar cuenta
st.subheader("Eliminar cuenta")
cuenta_eliminar = st.selectbox("Seleccione cuenta a eliminar:", opciones)
if st.button("Eliminar cuenta"):
    cuentas = [c for c in cuentas if c.numero_cuenta != cuenta_eliminar]
    st.session_state.cuentas = cuentas
    st.success(f"Cuenta {cuenta_eliminar} eliminada.")

# Reportes
st.subheader("Reportes del día")
total_depositos = sum(c.depositos_del_dia for c in cuentas)
total_retiros = sum(c.retiros_del_dia for c in cuentas)

st.write("### Depósitos por cuenta")
for c in cuentas:
    if c.depositos_del_dia > 0:
        st.write(f"Cuenta {c.numero_cuenta}: {c.depositos_del_dia:.2f}")

st.write("### Retiros por cuenta")
for c in cuentas:
    if c.retiros_del_dia > 0:
        st.write(f"Cuenta {c.numero_cuenta}: {c.retiros_del_dia:.2f}")

st.write("### Totales del día")
st.write(f"Total depositado: {total_depositos:.2f}")
st.write(f"Total retirado: {total_retiros:.2f}")

# Guardar al cierre
if st.button("Guardar cuentas"):
    guardar_cuentas(cuentas)
    st.success("Cuentas guardadas en cuentas.txt")
