import streamlit as st
import sympy as sp
import random
import re

def corregir_multiplicacion(expr_str):
    """
    Corrige expresiones donde falta el operador '*' entre número y variable o variables consecutivas.
    Ejemplo: '6x' -> '6*x', 'xy' -> 'x*y'.
    """
    expr_str = expr_str.replace(" ", "")  # eliminar espacios para evitar confusiones
    expr_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_str)
    expr_str = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr_str)
    return expr_str

def generador_ejercicios():
    st.header("🎯 Ejercicios Prácticos: Expansión y Factorización")

    # Inicialización segura del estado
    if "ejercicio_generado" not in st.session_state:
        st.session_state.ejercicio_generado = False

    if "modo" not in st.session_state:
        st.session_state.modo = "Expandir productos notables"

    if "nivel" not in st.session_state:
        st.session_state.nivel = "Básico"

    # Selección de modo y nivel (fuera de formularios para persistencia inmediata)
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

    x = sp.symbols('x')

    # Ejercicios ampliados: el doble en cada nivel y tipo
    ejercicios_expansion = {
        "Básico": [
            (x + 3)**2, (x - 5)**2, (x + 4)*(x - 4), (x + 2)**2, (x - 3)**2, (x + 1)*(x - 1)
        ],
        "Intermedio": [
            (2*x + 3)**2, (3*x - 1)**2, (4*x + 2)*(4*x - 2), (x - 2)**3, (5*x + 1)**2, (2*x - 5)**3
        ],
        "Avanzado": [
            (2*x + 3)**3, (3*x - 1)**3, ((x + 2)*(x - 2)) + (2*x + 1)**2,
            (x + 1)**3, (4*x - 3)**3, ((3*x + 2)*(3*x - 2)) + (x + 1)**2
        ],
    }

    ejercicios_factorizacion = {
        "Básico": [
            x**2 + 6*x + 9, x**2 - 16, x**2 - 10*x + 25,
            x**2 + 4*x + 4, x**2 - 9, x**2 - 6*x + 9
        ],
        "Intermedio": [
            9*x**2 - 30*x + 25, 4*x**2 - 25, x**3 - 6*x**2 + 12*x - 8,
            16*x**2 - 40*x + 25, 25*x**2 - 36, x**3 + 3*x**2 - 4*x - 12
        ],
        "Avanzado": [
            8*x**3 + 12*x**2 + 6*x + 1, 16*x**2 - 49, (x**2 - 4) + (4*x**2 + 4*x + 1),
            27*x**3 + 8, 64*x**3 - 125, x**3 + 6*x**2 + 12*x + 8
        ],
    }

    # Funciones para obtener un ejercicio al azar
    def generar_expansion(nivel):
        return random.choice(ejercicios_expansion[nivel])

    def generar_factorizacion(nivel):
        return random.choice(ejercicios_factorizacion[nivel])

    # Formulario para generar ejercicio nuevo
    with st.form(key="form_generar"):
        generar = st.form_submit_button("🔁 Generar nuevo ejercicio")
        if generar:
            if st.session_state.modo == "Expandir productos notables":
                st.session_state.expr = generar_expansion(st.session_state.nivel)
                st.session_state.solucion = sp.expand(st.session_state.expr)
            else:
                st.session_state.expr = generar_factorizacion(st.session_state.nivel)
                st.session_state.solucion = sp.factor(st.session_state.expr)
            st.session_state.ejercicio_generado = True
            st.session_state.respuesta_usuario = ""

    # Mostrar ejercicio actual si fue generado
    if st.session_state.ejercicio_generado:
        st.markdown(f"### 💡 Ejercicio de {st.session_state.modo} - Nivel {st.session_state.nivel}")
        st.latex(sp.latex(st.session_state.expr))

        # Formulario para responder y verificar
        with st.form(key="form_responder"):
            respuesta = st.text_input(
                "✍️ Ingresa tu respuesta (usa ^ o ** para potencias):",
                value=st.session_state.get("respuesta_usuario", ""),
                key="respuesta_input"
            )
            verificar = st.form_submit_button("✅ Verificar respuesta")

            if verificar:
                st.session_state.respuesta_usuario = respuesta  # Guardar respuesta

                if not respuesta.strip():
                    st.warning("⚠️ Por favor ingresa una respuesta antes de verificar.")
                else:
                    try:
                        entrada_limpia = corregir_multiplicacion(respuesta.replace("^", "**"))
                        entrada_usuario = sp.sympify(entrada_limpia)
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

                                st.markdown("### 🧠 Consejo pedagógico:")
                                if isinstance(st.session_state.expr, sp.Add):
                                    terms = list(st.session_state.expr.args)
                                    if len(terms) == 3:
                                        st.markdown("- ¿Podría ser un trinomio cuadrado perfecto?")
                                    elif any(t.has(sp.Symbol('x')**2) for t in terms) and any(t.has(sp.Symbol('x')**0) for t in terms):
                                        st.markdown("- ¿Existe una diferencia de cuadrados?")
                                    elif any(t.has(sp.Symbol('x')**3) for t in terms):
                                        st.markdown("- ¿Hay estructura de cubo perfecto?")

                    except Exception as e:
                        st.error(f"⚠️ No entendí tu expresión. Verifica paréntesis y operadores. Detalle técnico: {str(e)}")
    else:
        st.info("Haz clic en 'Generar nuevo ejercicio' para comenzar.")

def main():
    st.set_page_config(page_title="Aprende Factorización y Productos Notables", layout="wide")
    st.title("📚 Aprende Factorización y Productos Notables")
    st.markdown(
        """
        La **factorización** y los **productos notables** son fundamentales en álgebra para simplificar expresiones y resolver ecuaciones.
        Aquí puedes practicar la **expansión** y la **factorización** con ejercicios generados aleatoriamente y recibir retroalimentación inmediata.
        """
    )
    generador_ejercicios()

if __name__ == "__main__":
    main()

