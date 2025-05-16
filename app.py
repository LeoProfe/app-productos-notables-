def generador_ejercicios():
    st.header("🎯 Ejercicios Prácticos: Expansión y Factorización")

    modo = st.radio("¿Qué deseas practicar?", ["Expandir productos notables", "Aplicar factorización"], horizontal=True)

    niveles = ["Básico", "Intermedio", "Avanzado"]
    nivel = st.selectbox("📈 Nivel de dificultad:", niveles)

    x = sp.symbols('x')

    def generar_expansion(nivel):
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

    def generar_factorizacion(nivel):
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

    # Botón de generar
    if st.button("🔁 Generar nuevo ejercicio"):
        if modo == "Expandir productos notables":
            expr = generar_expansion(nivel)
            solucion = sp.expand(expr)
        else:
            expr = generar_factorizacion(nivel)
            solucion = sp.factor(expr)

        st.session_state["modo"] = modo
        st.session_state["nivel"] = nivel
        st.session_state["expr"] = expr
        st.session_state["solucion"] = solucion

    # Mostrar si hay un ejercicio activo
    if "expr" in st.session_state:
        st.markdown(f"### 💡 Ejercicio de {st.session_state['modo']} - Nivel {st.session_state['nivel']}")
        st.latex(sp.latex(st.session_state["expr"]))

        entrada = st.text_input("✍️ Ingresa tu respuesta (usa ^ o ** para potencias):", key="respuesta_usuario")

        if st.button("✅ Verificar respuesta"):
            try:
                entrada_usuario = sp.sympify(entrada.replace("^", "**"))
                solucion = st.session_state["solucion"]
                if modo == "Expandir productos notables":
                    es_correcto = sp.simplify(entrada_usuario - solucion) == 0
                else:
                    # Para factorización, debemos expandir la respuesta y comparar
                    es_correcto = sp.simplify(sp.expand(entrada_usuario) - sp.expand(st.session_state["expr"])) == 0

                if es_correcto:
                    st.success("🎉 ¡Correcto! Muy buen trabajo.")
                    st.balloons()
                else:
                    st.error("❌ La respuesta no es correcta.")
                    st.markdown("### ✅ Solución esperada:")
                    st.latex(sp.latex(solucion))

                    # Retroalimentación detallada
                    if modo == "Expandir productos notables":
                        st.info("👀 Verifica si distribuiste bien los términos y aplicaste correctamente las potencias.")
                    else:
                        st.info("🔍 Consejo: Intenta buscar factores comunes, diferencias de cuadrados o trinomios cuadrados perfectos.")
                        st.markdown("### 🛠️ Consejo pedagógico:")
                        if isinstance(st.session_state["expr"], sp.Add) and len(st.session_state["expr"].args) == 3:
                            st.markdown("- ¿Es un trinomio cuadrado perfecto?")
                        elif isinstance(st.session_state["expr"], sp.Add) and "**2" in str(st.session_state["expr"]):
                            st.markdown("- ¿Hay una diferencia de cuadrados?")
                        elif isinstance(st.session_state["expr"], sp.Add) and "**3" in str(st.session_state["expr"]):
                            st.markdown("- ¿Es un cubo perfecto? Revisa la fórmula del cubo de binomio.")
            except Exception as e:
                st.error(f"⚠️ No entendí tu expresión. Detalle técnico: {str(e)}")
    else:
        st.info("Haz clic en 'Generar nuevo ejercicio' para comenzar.")
