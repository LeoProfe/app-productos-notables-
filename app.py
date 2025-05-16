import streamlit as st
import random
import sympy as sp

# Configuración general
st.set_page_config(page_title="Factorización y Productos Notables", layout="wide")

# ---------- Introducción ----------
def intro():
    st.title("📘 Aprende Factorización y Productos Notables")
    st.markdown("""
    Bienvenido a esta plataforma interactiva de aprendizaje de **álgebra elemental**.  
    Aquí aprenderás a identificar y desarrollar los principales **productos notables** y a **factorizar expresiones algebraicas**.

    ### 🔎 ¿Qué aprenderás?
    - Las fórmulas fundamentales de productos notables
    - Cómo resolver paso a paso
    - Cómo aplicar estos conocimientos a ejercicios reales

    ---
    """)

# ---------- Teoría ----------
def teoria():
    st.subheader("📚 Teoría: Productos Notables")

    productos = {
        "Cuadrado de un binomio": r"(a \pm b)^2 = a^2 \pm 2ab + b^2",
        "Producto de binomios conjugados": r"(a+b)(a-b) = a^2 - b^2",
        "Cubo de un binomio": r"(a \pm b)^3 = a^3 \pm 3a^2b + 3ab^2 \pm b^3",
        "Suma por diferencia": r"(x+y)(x-y) = x^2 - y^2",
    }

    for nombre, formula in productos.items():
        with st.expander(f"🧠 {nombre}"):
            st.latex(formula)
            st.markdown(
                f"""
                Esta identidad nos permite simplificar expresiones algebraicas rápidamente y es clave en el desarrollo del pensamiento algebraico.
                """)
    st.info("💡 Consejo pedagógico: Memorizar fórmulas no es suficiente. Aprende a **reconocer patrones** y aplicarlos en diferentes contextos.")

# ---------- Ejercicio Guiado ----------
def ejercicio_guiado():
    st.subheader("👣 Ejercicio Guiado con Explicación Paso a Paso")

    ejercicios = [
        {"expr": "(x + 3)**2", "solucion": "x**2 + 6*x + 9", "descripcion": "Desarrollar el cuadrado del binomio (x + 3)^2"},
        {"expr": "(2*x - 5)**2", "solucion": "4*x**2 - 20*x + 25", "descripcion": "Desarrollar el cuadrado del binomio (2x - 5)^2"},
        {"expr": "(x + 4)*(x - 4)", "solucion": "x**2 - 16", "descripcion": "Multiplicar binomios conjugados (x + 4)(x - 4)"},
        {"expr": "(x - 2)**3", "solucion": "x**3 - 6*x**2 + 12*x - 8", "descripcion": "Desarrollar el cubo del binomio (x - 2)^3"},
    ]

    opcion = st.selectbox("🧮 Selecciona un ejercicio para resolver paso a paso:", [e["descripcion"] for e in ejercicios])
    ejercicio = next(e for e in ejercicios if e["descripcion"] == opcion)

    expr = sp.sympify(ejercicio['expr'])
    st.latex(f"\text{{Expresión: }} {sp.latex(expr)}")

    st.markdown("### 🔄 Paso 1: Expande la expresión")
    paso1 = sp.expand(expr)
    st.latex(sp.latex(paso1))

    st.markdown("### ✍️ Paso 2: Intenta escribir tú el resultado completo")
    respuesta_usuario = st.text_input("Escribe el resultado expandido (usa ^ o **):", key="resp_guiado")
    
    if st.button("✅ Verificar respuesta guiada"):
        try:
            respuesta_usuario = respuesta_usuario.replace("^", "**")
            resp_usuario = sp.sympify(respuesta_usuario)
            if sp.simplify(resp_usuario - paso1) == 0:
                st.success("¡Correcto! Has desarrollado correctamente el producto notable.")
            else:
                st.error("❌ La respuesta no es correcta. Revisa los términos.")
                st.markdown("✅ Resultado correcto:")
                st.latex(sp.latex(paso1))
        except Exception as e:
            st.error(f"⚠️ Error al interpretar tu respuesta: {str(e)}")

# ---------- Generador Aleatorio ----------
def generador_ejercicios():
    st.subheader("🎲 Práctica Aleatoria")

    tipos = ["Cuadrado de binomio", "Binomios conjugados", "Cubo de binomio"]

    def generar_cuadrado_binomio():
        x = sp.symbols('x')
        b = random.randint(1, 10)
        expr = (x + b)**2
        sol = sp.expand(expr)
        return expr, sol

    def generar_binomios_conjugados():
        x = sp.symbols('x')
        b = random.randint(1, 10)
        expr = (x + b)*(x - b)
        sol = sp.expand(expr)
        return expr, sol

    def generar_cubo_binomio():
        x = sp.symbols('x')
        b = random.randint(1, 5)
        expr = (x + b)**3
        sol = sp.expand(expr)
        return expr, sol

    tipo = st.selectbox("📌 Elige el tipo de ejercicio:", tipos)
    if tipo == "Cuadrado de binomio":
        expr, sol = generar_cuadrado_binomio()
    elif tipo == "Binomios conjugados":
        expr, sol = generar_binomios_conjugados()
    else:
        expr, sol = generar_cubo_binomio()

    st.markdown("### 📝 Ejercicio generado:")
    st.latex(f"{sp.latex(expr)}")

    respuesta = st.text_input("Escribe el resultado expandido:", key="resp_practico")

    if st.button("✅ Verificar respuesta práctica"):
        try:
            respuesta = respuesta.replace("^", "**")
            resp_usuario = sp.sympify(respuesta)
            if sp.simplify(resp_usuario - sol) == 0:
                st.success("¡Muy bien! Has resuelto el ejercicio correctamente.")
                st.balloons()
            else:
                st.error("Respuesta incorrecta.")
                st.markdown("✅ Resultado correcto:")
                st.latex(sp.latex(sol))
        except Exception:
            st.error("⚠️ No entendí tu expresión. Usa una expresión válida.")

# ---------- Layout Principal ----------
def main():
    intro()
    tab1, tab2, tab3 = st.tabs(["📘 Teoría", "🧠 Ejercicios Guiados", "🎯 Práctica Aleatoria"])
    with tab1:
        teoria()
    with tab2:
        ejercicio_guiado()
    with tab3:
        generador_ejercicios()

if __name__ == "__main__":
    main()
