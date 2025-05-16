import streamlit as st
import sympy as sp
import random

def generar_expansion(nivel, x):
    if nivel == "Básico":
        ejercicios = [
            (x + 3)**2,
            (x - 5)**2,
            (x + 4)*(x - 4),
        ]
    elif nivel == "Intermedio":
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        ejercicios = [
            (a*x + b)**2,
            (a*x - b)**2,
            (a*x + b)*(a*x - b),
            (x - 2)**3,
        ]
    else:  # Avanzado
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        ejercicios = [
            (a*x + b)**3,
            (a*x - b)**3,
            ((x + b)*(x - b)) + (a*x + b)**2,
        ]
    return random.choice(ejercicios)


def generar_factorizacion(nivel, x):
    if nivel == "Básico":
        ejercicios = [
            x**2 + 6*x + 9,
            x**2 - 16,
            x**2 - 10*x + 25,
        ]
    elif nivel == "Intermedio":
        ejercicios = [
            9*x**2 - 30*x + 25,
            4*x**2 - 25,
            x**3 - 6*x**2 + 12*x - 8,
        ]
    else:  # Avanzado
        ejercicios = [
            8*x**3 + 12*x**2 + 6*x + 1,
            16*x**2 - 49,
            (x**2 - 4) + (4*x**2 + 4*x + 1),
        ]
    return random.choice(ejercicios)


def generador_ejercicios():
    st.set_page_config(
        page_title="Práctica de Productos Notables y Factorización",
        page_icon="🧮",
        layout="centered",
    )

    st.title("🧮 Práctica de Productos Notables y Factorización")
    st.markdown("---")

    # --- TEORÍA RESUMIDA (Parte superior) ---
with st.expander("📚 Resumen Teórico (click para ver/ocultar)", expanded=True):
    st.markdown("""
    ### Productos Notables

    - **Cuadrado de binomio:**  
      \\[
      (a \\pm b)^2 = a^2 \\pm 2ab + b^2
      \\]

    - **Diferencia de cuadrados:**  
      \\[
      (a + b)(a - b) = a^2 - b^2
      \\]

    - **Cubo de binomio:**  
      \\[
      (a \\pm b)^3 = a^3 \\pm 3a^2b + 3ab^2 \\pm b^3
      \\]

    ### Factorización

    - **Factor común:** Extraer el factor común de todos los términos.  
      Ejemplo: \\( ax + ay = a(x + y) \\)

    - **Trinomio cuadrado perfecto:**  
      \\[
      a^2 \\pm 2ab + b^2 = (a \\pm b)^2
      \\]

    - **Diferencia de cuadrados:**  
      \\[
      a^2 - b^2 = (a + b)(a - b)
      \\]

    - **Suma y diferencia de cubos:**  
      \\[
      a^3 + b^3 = (a + b)(a^2 - ab + b^2)
      \\]  
      \\[
      a^3 - b^3 = (a - b)(a^2 + ab + b^2)
      \\]
    """, unsafe_allow_html=True)


    st.markdown("---")

    # Inicialización segura de sesión
    if "ejercicio_generado" not in st.session_state:
        st.session_state.ejercicio_generado = False
    if "modo" not in st.session_state:
        st.session_state.modo = "Expandir productos notables"
    if "nivel" not in st.session_state:
        st.session_state.nivel = "Básico"
    if "respuesta_usuario" not in st.session_state:
        st.session_state.respuesta_usuario = ""

    x = sp.symbols('x')

    # --- FORMULARIO INTEGRADO ---
    with st.form(key="form_practica", clear_on_submit=False):
        modo = st.radio(
            "¿Qué deseas practicar?", 
            ["Expandir productos notables", "Aplicar factorización"], 
            horizontal=True,
            index=["Expandir productos notables", "Aplicar factorización"].index(st.session_state.modo)
        )

        nivel = st.selectbox(
            "Nivel de dificultad:", 
            ["Básico", "Intermedio", "Avanzado"],
            index=["Básico", "Intermedio", "Avanzado"].index(st.session_state.nivel)
        )

        # Si se genera ejercicio nuevo, actualizamos el estado
        generar = st.form_submit_button("🔁 Generar nuevo ejercicio")

        if generar or not st.session_state.ejercicio_generado:
            if modo == "Expandir productos notables":
                expr = generar_expansion(nivel, x)
                solucion = sp.expand(expr)
            else:
                expr = generar_factorizacion(nivel, x)
                solucion = sp.factor(expr)

            st.session_state.update({
                "modo": modo,
                "nivel": nivel,
                "expr": expr,
                "solucion": solucion,
                "ejercicio_generado": True,
                "respuesta_usuario": "",
                "mensaje_retro": None,
                "resultado_verif": None,
            })

        if st.session_state.ejercicio_generado:
            st.markdown(f"### 💡 Ejercicio: {st.session_state.modo} - Nivel {st.session_state.nivel}")
            st.latex(sp.latex(st.session_state.expr))

            respuesta_usuario = st.text_input(
                "✍️ Ingresa tu respuesta (usa ^ o ** para potencias):",
                value=st.session_state.get("respuesta_usuario", ""),
                key="respuesta_input"
            )

            verificar = st.form_submit_button("✅ Verificar respuesta")

            if verificar:
                st.session_state.respuesta_usuario = respuesta_usuario.strip()
                try:
                    entrada_usuario = sp.sympify(st.session_state.respuesta_usuario.replace("^", "**"))
                    if st.session_state.modo == "Expandir productos notables":
                        correcto = sp.simplify(entrada_usuario - st.session_state.solucion) == 0
                    else:
                        # Para factorización, comparamos expandiendo ambas expresiones
                        correcto = sp.simplify(sp.expand(entrada_usuario) - sp.expand(st.session_state.expr)) == 0

                    if correcto:
                        st.session_state.resultado_verif = "correcto"
                        st.success("🎉 ¡Correcto! Excelente trabajo.")
                        st.balloons()
                    else:
                        st.session_state.resultado_verif = "incorrecto"
                        st.error("❌ Tu respuesta no es correcta.")
                        st.markdown("### ✅ Solución esperada:")
                        st.latex(sp.latex(st.session_state.solucion))

                        # Retroalimentación pedagógica
                        if st.session_state.modo == "Expandir productos notables":
                            st.info("📘 Consejo: Revisa si aplicaste correctamente la fórmula del cuadrado o cubo del binomio.")
                        else:
                            st.info("🔍 Intenta buscar patrones comunes: trinomios cuadrados, diferencia de cuadrados, cubos perfectos, etc.")

                            st.markdown("### 🧠 Consejo pedagógico:")
                            expr = st.session_state.expr
                            if isinstance(expr, sp.Add):
                                terms = list(expr.args)
                                if len(terms) == 3:
                                    st.markdown("- ¿Podría ser un trinomio cuadrado perfecto?")
                                elif any(t.has(x**2) for t in terms) and any(t.has(x**0) for t in terms):
                                    st.markdown("- ¿Existe una diferencia de cuadrados?")
                                elif any(t.has(x**3) for t in terms):
                                    st.markdown("- ¿Hay estructura de cubo perfecto?")
                except Exception as e:
                    st.error(f"⚠️ No entendí tu expresión. Verifica paréntesis y operadores. Detalle: {e}")

if __name__ == "__main__":
    generador_ejercicios()
