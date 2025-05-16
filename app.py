import streamlit as st
import random
import sympy as sp

st.set_page_config(page_title="Aprende Factorización y Productos Notables", layout="wide")

def intro():
    st.markdown("📚 Aprendamos Factorización y Productos Notables")
    st.latex("""
    La **factorización** y los **productos notables** son herramientas fundamentales en álgebra para simplificar expresiones y resolver ecuaciones.  
    Conocerlos bien permite acelerar cálculos y desarrollar el pensamiento algebraico.  
    Aquí aprenderás las fórmulas, verás ejemplos interactivos y practicarás con ejercicios.  
    """)
    st.latex("---")

def teoria():
    st.header("🔍 Teoría y Fórmulas de Productos Notables")

    productos = {
        "Cuadrado de un binomio": r"\((a \pm b)^2 = a^2 \pm 2ab + b^2\)",
        "Producto de binomios conjugados": r"\((a+b)(a-b) = a^2 - b^2\)",
        "Cubo de un binomio": r"\((a \pm b)^3 = a^3 \pm 3a^2b + 3ab^2 \pm b^3\)",
        "Suma por diferencia": r"\((x+y)(x-y) = x^2 - y^2\)",
    }

    for nombre, formula in productos.items():
        with st.expander(nombre):
            st.latex(formula)
            st.markdown(f"Esta fórmula nos permite transformar expresiones de la forma indicada, acelerando los cálculos.")
            # Podríamos agregar animaciones o gráficos si se quiere

def ejercicio_guiado():
    st.header("✏️ Ejercicios Guiados con Paso a Paso")

    ejercicios = [
        {
            "expr": "(x + 3)**2",
            "solucion": "x**2 + 6*x + 9",
            "descripcion": "Desarrollar el cuadrado del binomio (x + 3)^2"
        },
        {
            "expr": "(2*x - 5)**2",
            "solucion": "4*x**2 - 20*x + 25",
            "descripcion": "Desarrollar el cuadrado del binomio (2x - 5)^2"
        },
        {
            "expr": "(x + 4)*(x - 4)",
            "solucion": "x**2 - 16",
            "descripcion": "Multiplicar binomios conjugados (x + 4)(x - 4)"
        },
        {
            "expr": "(x - 2)**3",
            "solucion": "x**3 - 6*x**2 + 12*x - 8",
            "descripcion": "Desarrollar el cubo del binomio (x - 2)^3"
        }
    ]

    opcion = st.selectbox("Selecciona un ejercicio para ver paso a paso:", [e["descripcion"] for e in ejercicios])
    ejercicio = next(e for e in ejercicios if e["descripcion"] == opcion)

    st.latex(f"Expresión: {ejercicio['expr']}")
    expr = sp.sympify(ejercicio['expr'])
    st.markdown("Desarrollando la expresión paso a paso:")
    paso1 = sp.expand(expr)
    st.latex(sp.latex(paso1))

    st.markdown("¿Cuál es el resultado desarrollado?")
    respuesta_usuario = st.text_input("Escribe el resultado (en sintaxis Python o álgebra clásica)", key="resp_guiado")

    if st.button("Verificar respuesta guiada"):
        try:
            resp_usuario = sp.sympify(respuesta_usuario)
            if sp.simplify(resp_usuario - paso1) == 0:
                st.success("¡Correcto! Excelente trabajo.")
            else:
                st.error("La respuesta no es correcta, revisa los términos.")
                st.latex(sp.latex(paso1))
        except Exception as e:
            st.error("No entendí la respuesta, intenta con una expresión válida.")

def generador_ejercicios():
    st.header("🎲 Ejercicios Prácticos Aleatorios")

    tipos = ["Cuadrado de binomio", "Binomios conjugados", "Cubo de binomio"]

    def generar_cuadrado_binomio():
        a = sp.symbols('a')
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

    tipo = st.selectbox("Selecciona el tipo de ejercicio:", tipos)
    expr, sol = None, None
    if tipo == "Cuadrado de binomio":
        expr, sol = generar_cuadrado_binomio()
    elif tipo == "Binomios conjugados":
        expr, sol = generar_binomios_conjugados()
    else:
        expr, sol = generar_cubo_binomio()

    st.latex(f"Ejercicio: Expande la expresión {sp.latex(expr)}")

    respuesta = st.text_input("Escribe la expresión expandida (usa x y operadores +, -, *, **):", key="resp_practico")

    if st.button("Verificar respuesta práctica"):
        try:
            resp_usuario = sp.sympify(respuesta)
            if sp.simplify(resp_usuario - sol) == 0:
                st.success("¡Muy bien! Respuesta correcta.")
            else:
                st.error(f"Respuesta incorrecta. La solución correcta es: {sp.latex(sol)}")
        except Exception:
            st.error("No entendí la expresión. Por favor usa una expresión válida.")

def main():
    intro()
    teoria()
    ejercicio_guiado()
    generador_ejercicios()

if __name__ == "__main__":
    main()

