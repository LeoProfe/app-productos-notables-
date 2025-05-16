import streamlit as st
import sympy as sp
import random

st.set_page_config(page_title="Factorización y Productos Notables", layout="wide")

x = sp.symbols('x')

def generador_ejercicios():
    st.header("🎯 Ejercicios Prácticos: Expansión y Factorización")

    # Inicialización del estado
    if "ejercicio_generado" not in st.session_state:
        st.session_state.ejercicio_generado = False
    if "modo" not in st.session_state:
        st.session_state.modo = "Expandir productos notables"
    if "nivel" not in st.session_state:
        st.session_state.nivel = "Básico"
    if "respuesta_usuario" not in st.session_state:
        st.session_state.respuesta_usuario = ""
    if "generar_pulsado" not in st.session_state:
        st.session_state.generar_pulsado = False

    st.session_state.modo = st.radio(
        "¿Qué deseas practicar?",
        ["Expandir productos notables", "Aplicar factorización"],
        index=["Expandir productos notables", "Aplicar factorización"].index(st.session_state.modo),
        horizontal=True
    )

    st.session_state.nivel = st.selectbox(
        "📈 Nivel de dificultad:",
        ["Básico", "Intermedio", "Avanzado"],
        index=["Básico", "Intermedio", "Avanzado"].index(st.session_state.nivel)
    )

    def generar_expansion(nivel):
        if nivel == "Básico":
            return random.choice([(x + 3)**2, (x - 5)**2, (x + 4)*(x - 4)])
        elif nivel == "Intermedio":
            a = random.randint(2, 5)
            b = random.randint(1, 6)
            return random.choice([(a*x + b)**2, (a*x - b)**2, (a*x + b)*(a*x - b), (x - 2)**3])
        else:
            a = random.randint(2, 5)
            b = random.randint(1, 5)
            return random.choice([(a*x + b)**3, (a*x - b)**3, ((x + b)*(x - b)) + (a*x + b)**2])

    def generar_factorizacion(nivel):
        if nivel == "Básico":
            return random.choice([x**2 + 6*x + 9, x**2 - 16, x**2 - 10*x + 25])
        elif nivel == "Intermedio":
            return random.choice([9*x**2 - 30*x + 25, 4*x**2 - 25, x**3 - 6*x**2 + 12*x - 8])
        else:
            return random.choice([8*x**3 + 12*x**2 + 6*x + 1, 16*x**2 - 49, (x**2 - 4) + (4*x**2 + 4*x + 1)])

    # Botón para generar ejercicio (fuera de form para evitar problemas)
    if st.button("🔁 Generar nuevo ejercicio"):
        if st.session_state.modo == "Expandir productos notables":
            st.session_state.expr = generar_expansion(st.session_state.nivel)
            st.session_state.solucion = sp.expand(st.session_state.expr)
        else:
            st.session_state.expr = generar_factorizacion(st.session_state.nivel)
            st.session_state.solucion = sp.factor(st.session_state.expr)
        st.session_state.ejercicio_generado = True
        st.session_state.respuesta_usuario = ""
        st.session_state.generar_pulsado = True

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
                    correcto = sp.simplify(sp.expand(entrada_usuario) - sp.expand(st.session_state.expr)) == 0

                if correcto:
                    st.success("🎉 ¡Correcto! Excelente trabajo.")
                    st.balloons()
                else:
                    st.error("❌ Tu respuesta no es correcta.")
                    st.markdown("### ✅ Solución esperada:")
                    st.latex(sp.latex(st.session_state.solucion))

                    if st.session_state.modo == "Expandir productos notables":
                        st.info("📘 Consejo: Revisa si aplicaste correctamente la fórmula del cuadrado o cubo del binomio.")
                    else:
                        st.info("🔍 Intenta buscar patrones comunes: trinomios cuadrados, diferencia de cuadrados, cubos perfectos, etc.")

            except Exception as e:
                st.error(f"⚠️ No entendí tu expresión. Verifica paréntesis y operadores. Detalle: {str(e)}")
    else:
        st.info("Haz clic en 'Generar nuevo ejercicio' para comenzar.")


def main():
    st.title("🧠 Aprende Productos Notables y Factorización")
    generador_ejercicios()

if __name__ == "__main__":
    main()
