import streamlit as st
import sympy as sp
import random

# Debe ser la PRIMERA llamada en el archivo después de imports
st.set_page_config(
    page_title="Ejercicios de Productos Notables y Factorización",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="auto",
)

def mostrar_teoria():
    st.markdown("""
    # 📚 Productos Notables y Factorización

    **Productos Notables:**

    | Fórmula | Nombre |
    |:---------:|:--------:|
    | \\((a \\pm b)^2 = a^2 \\pm 2ab + b^2\\) | Cuadrado de binomio |
    | \\((a + b)(a - b) = a^2 - b^2\\) | Producto de suma por diferencia |
    | \\((a \\pm b)^3 = a^3 \\pm 3a^2b + 3ab^2 \\pm b^3\\) | Cubo de binomio |

    **Factorización:**

    - Factor común
    - Trinomio cuadrado perfecto
    - Diferencia de cuadrados
    - Suma y diferencia de cubos
    ---
    """)

def generador_ejercicios():
    st.header("🎯 Ejercicios Prácticos: Expansión y Factorización")

    # Opciones usuario
    modo = st.radio("¿Qué deseas practicar?", ["Expandir productos notables", "Aplicar factorización"], horizontal=True)
    nivel = st.selectbox("📈 Nivel de dificultad:", ["Básico", "Intermedio", "Avanzado"])

    x = sp.symbols('x')

    def generar_expansion(nivel):
        if nivel == "Básico":
            ejercicios = [
                (x + 3)**2,
                (x - 5)**2,
                (x + 4)*(x - 4),
                (2*x + 1)**2,
                (3*x - 2)**2,
                (x + 5)*(x - 5),
            ]
        elif nivel == "Intermedio":
            a = random.randint(2, 5)
            b = random.randint(1, 6)
            ejercicios = [
                (a*x + b)**2,
                (a*x - b)**2,
                (a*x + b)*(a*x - b),
                (x - 2)**3,
                (2*x + 3)**3,
                (3*x - 4)**3,
            ]
        else:  # Avanzado
            a = random.randint(2, 5)
            b = random.randint(1, 5)
            ejercicios = [
                (a*x + b)**3,
                (a*x - b)**3,
                ((x + b)*(x - b)) + (a*x + b)**2,
                (2*x + 1)**3 + (x - 2)**3,
                (3*x - 1)**3 - (x + 1)**3,
            ]
        return random.choice(ejercicios)

    def generar_factorizacion(nivel):
        if nivel == "Básico":
            ejercicios = [
                x**2 + 6*x + 9,
                x**2 - 16,
                x**2 - 10*x + 25,
                4*x**2 - 9,
                9*x**2 + 24*x + 16,
            ]
        elif nivel == "Intermedio":
            ejercicios = [
                9*x**2 - 30*x + 25,
                4*x**2 - 25,
                x**3 - 6*x**2 + 12*x - 8,
                8*x**3 + 27,
                x**3 + 27,
            ]
        else:  # Avanzado
            ejercicios = [
                8*x**3 + 12*x**2 + 6*x + 1,
                16*x**2 - 49,
                (x**2 - 4) + (4*x**2 + 4*x + 1),
                27*x**3 - 125,
                x**3 - 125,
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
                entrada_usuario = sp.sympify(st.session_state.respuesta_usuario.replace("^", "**"))
                if st.session_state.modo == "Expandir productos notables":
                    correcto = sp.simplify(entrada_usuario - st.session_state.solucion) == 0
                else:
                    # Para factorización comparamos la expansión para verificar equivalencia
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
