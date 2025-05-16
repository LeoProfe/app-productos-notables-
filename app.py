import streamlit as st
import sympy as sp
import random
import re

# Debe ser la PRIMERA llamada en el archivo después de imports
st.set_page_config(
    page_title="Ejercicios de Productos Notables y Factorización",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="auto",
)

def corregir_multiplicacion(expr_str):
    """
    Inserta el operador '*' donde falte entre coeficiente y variable.
    Ejemplo: "10x" -> "10*x", "3x^2" -> "3*x^2", "x2" -> "x*2"
    """
    # Inserta '*' entre dígito y letra
    expr_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_str)
    # Inserta '*' entre letra y dígito (por si acaso)
    expr_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr_str)
    return expr_str

def mostrar_teoria():
    st.markdown("""
    # 📚 Productos Notables

    | Nombre                      | Expresión algebraica                                            |
    |----------------------------|----------------------------------------------------------------|
    | **Cuadrado de binomio**    | (a ± b)² = a² ± 2ab + b²                                       |
    | **Producto suma-diferencia** | (a + b)(a - b) = a² - b²                                      |
    | **Cubo de binomio**        | (a ± b)³ = a³ ± 3a²b + 3ab² ± b³                               |
    | **Producto de binomios**   | (x - a)(x - b) = x² - (a + b)x + ab                            |
    """, unsafe_allow_html=True)

def generar_expansion(nivel):
    if nivel == "Básico":
        ejercicios = [
            (x + 1)**2,
            (x - 2)**2,
            (x + 3)*(x - 3),
            (x - 4)**2,
            (2*x + 1)**2,
            (x + 5)*(x - 5),
            (3*x - 2)**2,
            (x + 2)**2,
            (x - 1)*(x + 1),
            (2*x - 3)**2,
            (x + 4)**2,
            (x - 5)**2,
            (2*x + 2)*(2*x - 2),
            (x + 3)**2,
            (x - 3)**2,
            (3*x + 1)*(3*x - 1),
            (x + 6)*(x - 6),
            (x - 2)**2,
            (x + 2)*(x - 2),
            (2*x + 3)**2,
        ]
    elif nivel == "Intermedio":
        ejercicios = [
            (2*x + 3)**2,
            (3*x - 4)**2,
            (2*x + 5)*(2*x - 5),
            (4*x + 2)**2,
            (5*x - 1)**2,
            (x + 7)*(x - 7),
            (2*x - 3)**2,
            (x + 6)**2,
            (3*x + 5)*(3*x - 5),
            (x - 6)**2,
            (x + 4)*(x - 4),
            (4*x - 3)**2,
            (3*x + 1)*(3*x - 1),
            (5*x + 2)**2,
            (x - 7)**2,
            (2*x + 1)*(2*x - 1),
            (4*x + 5)**2,
            (3*x - 6)**2,
            (x + 8)*(x - 8),
            (6*x - 1)**2,
        ]
    else:  # Avanzado
        ejercicios = [
            (x + 4)**2 + (x - 3)*(x + 3),
            (3*x + 2)*(3*x - 2) + (x + 1)**2,
            (2*x + 5)**2,
            (x - 6)*(x + 6) + (x - 2)**2,
            (3*x - 1)**2,
            (x + 7)*(x - 7),
            (5*x + 2)**2 + (2*x - 1)*(2*x + 1),
            (4*x - 3)**2,
            (2*x + 3)*(2*x - 3),
            (x - 5)**2 + (x + 5)**2,
            (6*x + 1)*(6*x - 1),
            (x - 4)*(x + 4) + (x - 2)**2,
            (3*x + 1)*(3*x - 1),
            (2*x + 4)**2,
            (x + 3)**2 + (x - 3)**2,
            (5*x + 4)*(5*x - 4),
            (3*x - 2)**2 + (x + 1)*(x - 1),
            (4*x + 1)**2,
            (x - 7)**2 + (x + 2)**2,
            (6*x + 5)*(6*x - 5),
        ]
    return random.choice(ejercicios)

def generar_factorizacion(nivel):
    if nivel == "Básico":
        ejercicios = [
            x**2 + 2*x + 1,
            x**2 - 4,
            x**2 + 6*x + 9,
            4*x**2 - 9,
            x**2 + 10*x + 25,
            x**2 - 36,
            9*x**2 - 1,
            x**2 + 4*x + 4,
            x**2 - 2*x + 1,
            25*x**2 - 100,
            x**2 - 49,
            16*x**2 - 64,
            x**2 - 1,
            36*x**2 - 49,
            x**2 + 8*x + 16,
            49*x**2 - 81,
            64*x**2 - 36,
            x**2 + 12*x + 36,
            x**2 + 14*x + 49,
            9*x**2 + 12*x + 4,
        ]
    elif nivel == "Intermedio":
        ejercicios = [
            4*x**2 - 25,
            x**2 + 12*x + 36,
            9*x**2 - 30*x + 25,
            36*x**2 - 49,
            16*x**2 - 1,
            x**2 - 64,
            25*x**2 - 20*x + 4,
            x**2 + 9*x + 20,  # trinomio factorizable
            49*x**2 - 16,
            81*x**2 - 4,
            16*x**2 + 40*x + 25,
            4*x**2 + 28*x + 49,
            3*x**2 - 12*x + 12,
            x**2 + 11*x + 30,
            5*x**2 + 20*x + 15,
            4*x**2 - 36,
            49*x**2 - 1,
            x**2 + 6*x + 5,
            x**2 + 7*x + 6,
            x**2 - 8*x + 15,
        ]
    else:  # Avanzado
        ejercicios = [
            36*x**2 + 48*x + 16,
            4*x**2 - 1 + x**2 + 4*x + 4,
            (2*x - 1)**2 + (x + 3)*(x - 3),
            x**2 + 10*x + 25 + 4*x**2 - 9,
            49*x**2 - 36 + x**2 + 6*x + 9,
            (3*x + 2)*(3*x - 2) + (x - 2)**2,
            (5*x - 3)**2,
            (x - 6)*(x + 6) + (x - 1)**2,
            x**2 + 8*x + 16 + x**2 - 4,
            (2*x - 5)**2 + (2*x + 5)**2,
            (4*x + 3)**2 + (x - 4)*(x + 4),
            (5*x - 2)**2,
            (x + 5)*(x - 5) + x**2 + 4*x + 4,
            x**2 + 6*x + 9 + 4*x**2 - 1,
            (6*x + 5)*(6*x - 5),
            (3*x + 2)*(3*x - 2),
            16*x**2 - 64 + x**2 + 2*x + 1,
            36*x**2 + 60*x + 25,
            x**2 + 14*x + 49 + x**2 - 4,
            (7*x - 2)**2,
        ]
    return random.choice(ejercicios)


    # Guardar ejercicio en sesión para persistencia
    if "ejercicio_generado" not in st.session_state:
        st.session_state.ejercicio_generado = False
        st.session_state.respuesta_usuario = ""

    if st.button("🔁 Generar nuevo ejercicio"):
        if modo == "Expandir productos notables":
            st.session_state.expr = generar_expansion(nivel)
            st.session_state.solucion = sp.expand(st.session_state.expr)
        else:
            st.session_state.expr = generar_factorizacion(nivel)
            st.session_state.solucion = sp.factor(st.session_state.expr)

        st.session_state.modo = modo
        st.session_state.nivel = nivel
        st.session_state.ejercicio_generado = True
        st.session_state.respuesta_usuario = ""

    if st.session_state.ejercicio_generado:
        st.markdown(f"### 💡 Ejercicio de {st.session_state.modo} - Nivel {st.session_state.nivel}")
        st.latex(sp.latex(st.session_state.expr))

        st.session_state.respuesta_usuario = st.text_input(
            "✍️ Ingresa tu respuesta (usa ^ o ** para potencias):",
            value=st.session_state.respuesta_usuario,
            key="respuesta_input"
        )

        if st.button("✅ Verificar respuesta"):
            try:
                entrada_usuario = st.session_state.respuesta_usuario.replace("^", "**")
                entrada_usuario = corregir_multiplicacion(entrada_usuario)
                entrada_usuario = sp.sympify(entrada_usuario)

                if st.session_state.modo == "Expandir productos notables":
                    correcto = sp.simplify(entrada_usuario - st.session_state.solucion) == 0
                else:
                    correcto = sp.simplify(sp.expand(entrada_usuario) - sp.expand(st.session_state.expr)) == 0

                if correcto:
                    st.success("🎉 ¡Correcto! Excelente trabajo.")
                    st.balloons()
                else:
                    st.error("❌ Tu respuesta no es correcta.")
                    st.markdown("### ✅ Solución esperada:")
                    st.latex(sp.latex(st.session_state.solucion))
                    if st.session_state.modo == "Expandir productos notables":
                        st.info("📘 Consejo: Revisa si aplicaste correctamente la fórmula del binomio al cuadrado o cubo.")
                    else:
                        st.info("🔍 Intenta identificar factores comunes, diferencia de cuadrados, o cubos perfectos.")

            except Exception as e:
                st.error(f"⚠️ No entendí tu expresión. Verifica paréntesis y operadores. Detalle: {str(e)}")
    else:
        st.info("Haz clic en 'Generar nuevo ejercicio' para comenzar.")

def main():
    mostrar_teoria()
    st.markdown("---")
    generador_ejercicios()

if __name__ == "__main__":
    main()
