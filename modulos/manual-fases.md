# MANUAL-FASES.md — Banco de preguntas y reglas por fase (v4.0)

> Complemento de `AGENTS.md`. Define **qué se cubre, en qué orden y con qué criterio se aprueba**.
> Formato de cada ítem: `**N.X** [★] Etiqueta — pregunta guía`. El orden de este archivo es el **orden canónico**.

**Cómo se usa (v4)**
- **★ = núcleo humano (63 ítems):** solo el usuario lo sabe o lo decide (hechos de la organización, preferencias, recursos, permisos). Si no hay base en los archivos, el agente lo pregunta (máximo 3 por turno, con opciones).
- **Sin ★ (226 ítems):** el agente propone la respuesta a partir de lo aprobado, la evidencia y el buen oficio; el usuario aprueba con `ok` o corrige. Si no hay ninguna base, se pregunta igual que un ★.
- Se trabaja **por lotes** (una fase, o bloques de hasta 10 ítems). Nada que ya esté en los archivos se vuelve a preguntar.
- La pregunta guía orienta; el agente la adapta al proyecto y nunca la lee de forma mecánica.

---

## BLOQUE 1 · INICIO Y ADMISIÓN (Fases 0-2)

### Fase 0 · Configuración de la conversación
*Objetivo: definir cómo se desarrollará el trabajo. Los ★ se piden en un solo mensaje de arranque; el resto lo propone el agente.*

- **0.1** ★ Nombre provisional del proyecto — ¿Cómo se llama provisionalmente el proyecto (y su subtítulo, si lo tiene)?
- **0.2** ★ Organización o equipo solicitante — ¿Qué organización o equipo solicita la investigación?
- **0.3** ★ Persona que responde — ¿Quién responde este cuestionario?
- **0.4** Rol de esa persona — ¿Qué rol cumple en el proyecto?
- **0.5** Experiencia metodológica — ¿Qué nivel de experiencia metodológica tiene (básico, intermedio, avanzado)?
- **0.6** ★ Tipo de apoyo esperado — ¿Qué espera del agente: diseño completo, revisión, acompañamiento o formación?
- **0.7** Idioma de los entregables — ¿En qué idioma deben quedar los entregables?
- **0.8** Nivel de profundidad — ¿Qué profundidad busca: exploratoria, descriptiva, explicativa o propositiva?
- **0.9** ★ Fecha límite — ¿Existe una fecha límite conocida o el proyecto es recurrente?
- **0.10** Formato final — ¿Qué formato final espera (informe, presentación, dashboard, fichas, otro)?

### Fase 1 · Admisión del caso
*Objetivo: determinar si existe una necesidad real que justifique investigar.*

- **1.1** ★ Situación de origen — ¿Qué situación originó la solicitud?
- **1.2** ★ Necesidad a resolver — ¿Qué necesita resolver la organización?
- **1.3** ★ Urgencia actual — ¿Por qué es importante resolverlo ahora?
- **1.4** Costo de no investigar — ¿Qué sucedería si no se realiza la investigación?
- **1.5** ★ Intentos previos — ¿Qué se ha intentado anteriormente?
- **1.6** ★ Información existente — ¿Qué información existe ya?
- **1.7** Información faltante — ¿Qué información falta?
- **1.8** ★ Permiso de tratamiento — ¿Existe permiso para procesar la información?
- **1.9** ★ Propietario de la necesidad — ¿Quién es el propietario de la necesidad?
- **1.10** Viabilidad — ¿La investigación es viable dentro de las restricciones conocidas?

> **→ Gate G0 · Admisión** (ver *Gates*).

### Fase 2 · Definición de la decisión
*Objetivo: convertir una solicitud ambigua en una decisión estructurada.*

- **2.1** ★ Decisión a tomar — ¿Qué decisión deberá tomarse?
- **2.2** ★ Autoridad — ¿Quién tiene autoridad para tomarla?
- **2.3** Responsable de implementar — ¿Quién la implementará?
- **2.4** ★ Momento de la decisión — ¿Cuándo debe tomarse?
- **2.5** ★ Alternativas — ¿Qué alternativas existen?
- **2.6** ★ Alternativa implícita — ¿Qué alternativa parece preferirse hoy?
- **2.7** Criterios de comparación — ¿Con qué criterios se compararán las alternativas?
- **2.8** Costo del error — ¿Qué consecuencias tendría una decisión equivocada?
- **2.9** Reversibilidad — ¿La decisión es reversible?
- **2.10** Impacto — ¿Cuál es su nivel de impacto?
- **2.11** Urgencia — ¿Cuál es su nivel de urgencia?
- **2.12** ★ Incertidumbre crítica — ¿Qué incertidumbre impide decidir hoy?
- **2.13** Evidencia que la reduce — ¿Qué evidencia ayudaría a reducir esa incertidumbre?
- **2.14** Información irrelevante — ¿Qué información no cambiaría la decisión?
- **2.15** ★ Restricciones — ¿Qué restricciones condicionan la decisión?

**Detección activa de defectos:** varias decisiones en una solicitud · soluciones prematuras · actividades formuladas como objetivos · decisiones sin propietario · decisiones ya tomadas antes de investigar · criterios ausentes · fechas incompatibles · investigación pedida solo para justificar una posición previa.

> **Síntesis del Bloque 1:** el último lote incluye el *Decision Case* inicial. Sin aprobación aparte.

---

## BLOQUE 2 · ENMARCADO (Fases 3-4)

### Fase 3 · Contexto y problema de investigación
*Objetivo: traducir la necesidad decisional en un problema investigable.*

- **3.1** Contexto organizacional — ¿En qué contexto organizacional surge el estudio?
- **3.2** Contexto del entorno — ¿Qué pasa en el mercado o entorno que lo hace pertinente?
- **3.3** Antecedentes — ¿Qué antecedentes existen?
- **3.4** ★ Poblaciones afectadas — ¿Qué poblaciones se ven afectadas?
- **3.5** Comportamientos observados — ¿Qué comportamientos se han observado?
- **3.6** Síntomas — ¿Qué síntomas (manifestaciones observables) hay?
- **3.7** Posibles causas — ¿Qué causas hipotéticas se manejan?
- **3.8** Información disponible — ¿Qué información está disponible?
- **3.9** Calidad de la información — ¿Qué tan confiable y actual es esa información?
- **3.10** Brecha de conocimiento — ¿Qué no se sabe y se necesita saber?
- **3.11** ★ Alcance geográfico — ¿Qué territorios cubre el estudio y qué contrastes territoriales importan?
- **3.12** ★ Alcance temporal — ¿Qué periodo cubre el estudio?
- **3.13** ★ Alcance temático — ¿Qué dimensiones temáticas cubre el estudio?
- **3.14** ★ Exclusiones — ¿Qué queda explícitamente fuera?
- **3.15** Formulación del problema — ¿Cuál es la formulación final del problema de investigación?
- **3.16** Justificación y viabilidad — ¿Por qué vale la pena investigarlo y con qué fuentes es viable?

**Distinción obligatoria (nunca combinarlos como equivalentes):** problema empresarial (lo que duele) · problema de decisión (lo que hay que elegir) · problema de investigación (lo que hay que conocer) · síntoma (lo observable) · causa hipotética (explicación tentativa) · solución propuesta (respuesta prematura).

### Fase 4 · Audiencias y uso de resultados
*Objetivo: definir quién usará los resultados y cómo.*

- **4.1** ★ Usuario principal — ¿Quién es el usuario principal de los resultados?
- **4.2** Usuarios secundarios — ¿Quiénes más los usarán?
- **4.3** ★ Patrocinador — ¿Quién patrocina el estudio?
- **4.4** Propietario de la decisión — ¿Quién es dueño de la decisión?
- **4.5** ★ Aprobadores — ¿Quién aprueba los entregables?
- **4.6** Áreas interesadas — ¿Qué áreas tienen interés?
- **4.7** Personas afectadas — ¿Quiénes se verán afectados por los resultados?
- **4.8** Uso previsto — ¿Para qué se usarán los hallazgos?
- **4.9** Formato requerido — ¿En qué formato los necesita cada audiencia?
- **4.10** Nivel de detalle — ¿Qué nivel de detalle requiere cada audiencia?
- **4.11** ★ Sensibilidad — ¿Hay sensibilidad política u organizacional?
- **4.12** ★ Restricciones de comunicación — ¿Qué restricciones hay para comunicar resultados?
- **4.13** Acciones derivadas — ¿Qué acciones podrían derivarse de los hallazgos?
- **4.14** Mapa de conocimiento — ¿Cuál es el estado del arte (taxonomía, evidencia y vacíos) que enmarca el estudio?

> **Síntesis del Bloque 2:** el último lote incluye el enmarcado consolidado. Sin aprobación aparte.

---

## BLOQUE 3 · CONOCIMIENTO (Fases 5-6)

### Fase 5 · Objetivos de investigación
*Objetivo: definir qué deberá producir intelectualmente el estudio.*

- **5.1** Objetivo general — ¿Cuál es el objetivo general?
- **5.2** Objetivos específicos — ¿Cuáles son los objetivos específicos?
- **5.3** Resultado por objetivo — ¿Qué resultado de conocimiento entrega cada objetivo?
- **5.4** Relación con la decisión — ¿Cómo alimenta cada objetivo la decisión?
- **5.5** ★ Priorización — ¿En qué orden de prioridad se ubican?
- **5.6** ★ Objetivos obligatorios — ¿Cuáles son imprescindibles?
- **5.7** Objetivos deseables — ¿Cuáles son deseables pero sacrificables?
- **5.8** Exclusiones de objetivos — ¿Qué no pretende lograr el estudio?

**Auditoría de objetivos:** formulados como resultados de conocimiento (no actividades) · no anticipan conclusiones · pueden responderse con evidencia · contribuyen a la decisión · no se duplican · son viables. El agente aplica esta auditoría a su propia propuesta antes de entregar el lote.

### Fase 6 · Preguntas, hipótesis y supuestos
*Objetivo: transformar los objetivos en preguntas investigables.*

- **6.1** Pregunta principal — ¿Cuál es la pregunta principal?
- **6.2** Preguntas secundarias — ¿Cuáles son las preguntas secundarias?
- **6.3** Preguntas por objetivo — ¿Qué preguntas responde cada objetivo específico?
- **6.4** ★ Hipótesis — ¿Qué hipótesis (principal y secundarias) se plantean, cuando corresponda?
- **6.5** Supuestos — ¿Qué supuestos se asumen?
- **6.6** Explicaciones alternativas — ¿Qué explicaciones rivales podrían dar cuenta del mismo fenómeno?
- **6.7** Evidencia a favor — ¿Qué evidencia apoyaría cada hipótesis?
- **6.8** Evidencia en contra — ¿Qué evidencia la contradiría?
- **6.9** Información necesaria — ¿Qué información se necesita para responder cada pregunta?
- **6.10** Prioridad de preguntas — ¿Qué prioridad tiene cada pregunta?

**Búsqueda activa de defectos:** hipótesis no contrastables · preguntas que no aportan a la decisión · supuestos presentados como hechos · preguntas duplicadas, demasiado amplias o inductivas · explicaciones alternativas omitidas.

> **→ Gate G1 · Definición** (ver *Gates*).

---

## BLOQUE 4 · DISEÑO METODOLÓGICO (Fases 7-11)

### Fase 7 · Conceptos, variables y categorías
*Regla: no fuerces variables cuantitativas en un estudio exploratorio ni categorías rígidas en un diseño cualitativo emergente.*

- **7.1** Constructos principales — ¿Cuáles son los constructos centrales?
- **7.2** Dimensiones — ¿En qué dimensiones se descompone cada constructo?
- **7.3** Variables — ¿Qué variables operacionalizan esas dimensiones?
- **7.4** Categorías cualitativas iniciales — ¿Qué categorías iniciales guían el análisis cualitativo?
- **7.5** Indicadores — ¿Qué indicadores observables tiene cada variable?
- **7.6** Comportamientos observables — ¿Qué conductas se observarán?
- **7.7** Percepciones — ¿Qué percepciones interesa capturar?
- **7.8** Motivaciones — ¿Qué motivaciones se explorarán?
- **7.9** Barreras — ¿Qué barreras se explorarán?
- **7.10** Facilitadores — ¿Qué facilitadores se explorarán?
- **7.11** Experiencias — ¿Qué experiencias interesan?
- **7.12** Contextos — ¿Qué contextos condicionan el fenómeno?
- **7.13** Definiciones operativas — ¿Cómo se define operativamente cada concepto?
- **7.14** Relaciones esperadas — ¿Qué relaciones se esperan entre variables o categorías?
- **7.15** Aspectos abiertos — ¿Qué debe quedar abierto al descubrimiento?

### Fase 8 · Evidencia requerida

- **8.1** Tipo de evidencia — ¿Qué tipo de evidencia se necesita (numérica, narrativa, documental, observacional)?
- **8.2** Fuente potencial — ¿De qué fuentes puede venir?
- **8.3** Profundidad — ¿Con qué profundidad?
- **8.4** Comparaciones — ¿Qué comparaciones son necesarias?
- **8.5** Segmentos requeridos — ¿Para qué segmentos?
- **8.6** Cobertura — ¿Qué cobertura se requiere?
- **8.7** Actualidad — ¿Qué tan reciente debe ser?
- **8.8** ★ Nivel de confianza — ¿Qué nivel de confianza se espera?
- **8.9** Criterio de suficiencia — ¿Cuándo será suficiente la evidencia?
- **8.10** Contradicciones a buscar — ¿Qué contradicciones deben buscarse activamente?
- **8.11** Evidencia reutilizable — ¿Qué evidencia existente se puede reutilizar?
- **8.12** Evidencia faltante — ¿Qué evidencia falta?
- **8.13** Dependencia de una fuente — ¿Qué riesgo hay de depender de una sola fuente?
- **8.14** Deuda de evidencia — ¿Qué deuda de evidencia preexistente arrastra el proyecto?

### Fase 9 · Selección del enfoque metodológico
*No preguntes "¿qué método deseas usar?". 9.1 y 9.2 los resuelve el agente: compara alternativas (evidencia que producen, preguntas que responden, ventajas, limitaciones, riesgos, tiempo, complejidad y encaje con las restricciones) y recomienda una. 9.3 ★ lo elige el usuario entre 2-3 opciones.*
*Diseños a considerar: cualitativo, cuantitativo, mixto, exploratorio, descriptivo, explicativo, evaluativo, secuencial, concurrente, documental. Técnicas: entrevistas, grupos focales, etnografía, observación, diarios, comunidades en línea, encuestas, experimentos, análisis secundario, talleres de cocreación.*

- **9.1** Tipos de diseño evaluados — ¿Qué diseños son candidatos y cómo se comparan?
- **9.2** Técnicas evaluadas — ¿Qué técnicas son candidatas y cómo se comparan?
- **9.3** ★ Diseño seleccionado — ¿Qué diseño y técnicas se eligen, y por qué?

### Fase 10 · Población, segmentos y muestra
*Regla: nunca justifiques una muestra cualitativa solo con una cifra fija; relaciónala con heterogeneidad, objetivos, segmentos, profundidad y criterio de suficiencia.*

- **10.1** Población de interés — ¿Cuál es la población de interés?
- **10.2** Unidad de análisis — ¿Cuál es la unidad de análisis?
- **10.3** Unidad de observación — ¿Cuál es la unidad de observación?
- **10.4** Segmentos — ¿Qué segmentos se distinguen?
- **10.5** Criterios de inclusión — ¿Quién entra?
- **10.6** Criterios de exclusión — ¿Quién no entra?
- **10.7** Variables de segmentación — ¿Con qué variables se segmenta?
- **10.8** Casos críticos — ¿Qué casos son críticos?
- **10.9** Casos extremos — ¿Qué casos extremos conviene incluir?
- **10.10** Casos negativos — ¿Qué casos podrían refutar las hipótesis?
- **10.11** Distribución geográfica — ¿Cómo se distribuye la muestra en el territorio?
- **10.12** ★ Canales de acceso — ¿Por qué canales se accede a los participantes?
- **10.13** Disponibilidad — ¿Qué disponibilidad tienen?
- **10.14** Dificultad de reclutamiento — ¿Qué tan difícil será reclutarlos?
- **10.15** ★ Tamaño de muestra — ¿Qué tamaño de muestra se propone?
- **10.16** Justificación del tamaño — ¿Cómo se justifica?
- **10.17** Riesgos de representación — ¿Qué sesgos de representación hay?
- **10.18** Sustituciones — ¿Qué sustituciones se permiten?
- **10.19** Ampliar o detener — ¿Con qué criterio se amplía o detiene la muestra?
- **10.20** Saturación o poder — ¿Qué criterio de suficiencia aplica (saturación, poder estadístico, otro)?

### Fase 11 · Técnicas e instrumentos
*Definir para cada técnica. Construye los instrumentos solo después de aprobar su estructura: sin preguntas dobles ni inductivas, con sondas, separando preguntas principales y de profundización, cada pregunta ligada a un objetivo, preguntas sensibles identificadas, duración estimada e instrucciones de moderación.*

- **11.1** Propósito — ¿Para qué sirve cada técnica?
- **11.2** Objetivos cubiertos — ¿Qué objetivos cubre?
- **11.3** Preguntas cubiertas — ¿Qué preguntas de investigación cubre?
- **11.4** Participantes — ¿Con quiénes se aplica?
- **11.5** ★ Modalidad — ¿Presencial, virtual o mixta?
- **11.6** ★ Duración — ¿Cuánto dura?
- **11.7** Estructura — ¿Cuál es su estructura general?
- **11.8** Módulos — ¿Qué módulos contiene?
- **11.9** Estímulos — ¿Qué estímulos o materiales usa?
- **11.10** Técnicas proyectivas o interactivas — ¿Se usan? ¿Cuáles?
- **11.11** ★ Lenguaje — ¿Qué registro de lenguaje se usará con los participantes?
- **11.12** Riesgos de sesgo — ¿Qué sesgos puede introducir el instrumento?
- **11.13** ★ Prueba piloto — ¿Cómo se pilotea?
- **11.14** Protocolo de aplicación — ¿Cuál es el protocolo de aplicación?
- **11.15** Evidencia producida — ¿Qué evidencia produce cada técnica?

> **Síntesis del Bloque 4:** el último lote incluye el diseño metodológico consolidado. Sin aprobación aparte.

---

## BLOQUE 5 · TRAZABILIDAD Y ANÁLISIS (Fases 12-13)

### Fase 12 · Matriz de trazabilidad
*Objetivo: comprobar que todo elemento del diseño está conectado.*
*Cadena: Decisión → Incertidumbre → Objetivo → Pregunta de investigación → Evidencia → Método → Segmento → Instrumento → Pregunta del instrumento → Estrategia de análisis → Entregable → Uso esperado. El agente construye la matriz (12.1) y revisa él mismo las brechas (12.2-12.9): las presenta todas en un lote, cada una con su solución propuesta.*

- **12.1** Matriz construida — ¿La matriz completa está construida y revisada?
- **12.2** Objetivos sin preguntas — ¿Hay objetivos sin preguntas?
- **12.3** Preguntas sin método — ¿Hay preguntas sin método?
- **12.4** Métodos sin justificación — ¿Hay métodos sin justificación?
- **12.5** Segmentos sin propósito — ¿Hay segmentos sin propósito?
- **12.6** Preguntas de instrumento sin objetivo — ¿Hay preguntas de instrumento sin objetivo?
- **12.7** Objetivos sin cobertura instrumental — ¿Hay objetivos sin cobertura instrumental?
- **12.8** Evidencia sin uso — ¿Hay evidencia sin uso previsto?
- **12.9** Entregables sin decisión — ¿Hay entregables que no responden a la decisión?

### Fase 13 · Plan de análisis
*Distinción obligatoria: dato observado · evidencia · hallazgo · interpretación · hipótesis · inferencia · insight · recomendación · predicción.*

- **13.1** Unidad de análisis — ¿Sobre qué unidad se analiza?
- **13.2** Preparación de datos — ¿Cómo se preparan los datos?
- **13.3** ★ Transcripción — ¿Cómo y quién transcribe?
- **13.4** ★ Anonimización — ¿Cómo se anonimiza?
- **13.5** Codificación — ¿Qué estrategia de codificación se usa?
- **13.6** Libro de códigos — ¿Cómo se construye el libro de códigos?
- **13.7** Análisis temático — ¿Cómo se hace el análisis temático?
- **13.8** Comparación de segmentos — ¿Cómo se comparan los segmentos?
- **13.9** Triangulación — ¿Qué fuentes o métodos se triangulan?
- **13.10** Casos negativos — ¿Cómo se tratan los casos negativos?
- **13.11** Contradicciones — ¿Cómo se manejan las contradicciones?
- **13.12** Análisis estadístico — ¿Qué análisis estadístico aplica, si aplica?
- **13.13** Integración de métodos — ¿Cómo se integran los métodos?
- **13.14** ★ Revisión entre analistas — ¿Habrá revisión cruzada entre analistas?
- **13.15** Criterios de calidad — ¿Qué criterios de calidad se aplican?
- **13.16** Criterios de suficiencia — ¿Cuándo se considera suficiente el análisis?
- **13.17** Estructura de hallazgos — ¿Cómo se estructurarán los hallazgos?
- **13.18** Construcción de insights — ¿Cómo se construyen los insights?
- **13.19** Nivel de confianza — ¿Cómo se reporta la confianza de cada hallazgo?
- **13.20** Limitaciones interpretativas — ¿Qué límites tiene la interpretación?

> **→ Gate G2 · Diseño** (ver *Gates*).

---

## BLOQUE 6 · OPERACIÓN DE CAMPO (Fases 14-18)

### Fase 14 · Operación y trabajo de campo

- **14.1** Fases operativas — ¿En qué fases se organiza el campo?
- **14.2** Actividades — ¿Qué actividades incluye cada fase?
- **14.3** ★ Responsables — ¿Quién responde por cada actividad?
- **14.4** Dependencias — ¿Qué depende de qué?
- **14.5** Reclutamiento — ¿Cómo se recluta?
- **14.6** Contacto — ¿Cómo se contacta a los participantes?
- **14.7** Filtros — ¿Qué filtros se aplican?
- **14.8** Confirmaciones — ¿Cómo se confirma la asistencia?
- **14.9** Agendamiento — ¿Cómo se agenda?
- **14.10** Logística — ¿Qué logística requiere?
- **14.11** ★ Plataformas — ¿Qué plataformas se usan?
- **14.12** Grabación — ¿Cómo se graba?
- **14.13** ★ Incentivos — ¿Qué incentivos se ofrecen?
- **14.14** ★ Proveedores — ¿Qué proveedores intervienen?
- **14.15** Supervisión — ¿Cómo se supervisa?
- **14.16** Control de calidad — ¿Cómo se controla la calidad?
- **14.17** Manejo de ausencias — ¿Qué pasa si alguien no asiste?
- **14.18** Sustituciones — ¿Cómo se sustituyen participantes?
- **14.19** Incidentes — ¿Cómo se manejan incidentes?
- **14.20** Cierre de campo — ¿Cuándo y cómo se cierra el campo?

### Fase 15 · Ética, privacidad y gobierno
*Regla: si detectas un riesgo crítico, detén el avance de esa parte y explica qué debe resolverse.*

- **15.1** Datos personales — ¿Qué datos personales se recogen?
- **15.2** Datos sensibles — ¿Hay datos sensibles?
- **15.3** Poblaciones vulnerables — ¿Participan poblaciones vulnerables?
- **15.4** Consentimiento — ¿Cómo se obtiene el consentimiento?
- **15.5** Finalidad del tratamiento — ¿Para qué se tratan los datos?
- **15.6** Grabación — ¿Qué se graba y con qué autorización?
- **15.7** Uso de imagen o voz — ¿Se usará imagen o voz? ¿Cómo?
- **15.8** Anonimización — ¿Cómo se anonimiza?
- **15.9** ★ Acceso — ¿Quién accede a los datos?
- **15.10** ★ Almacenamiento — ¿Dónde se almacenan?
- **15.11** ★ Retención — ¿Cuánto tiempo se conservan?
- **15.12** Eliminación — ¿Cómo se eliminan?
- **15.13** ★ Transferencia a terceros — ¿Se transfieren a terceros?
- **15.14** ★ Uso de herramientas de IA — ¿Qué herramientas de IA tocan los datos y con qué salvaguardas?
- **15.15** ★ Restricciones del cliente — ¿Qué restricciones impone el cliente?
- **15.16** ★ Publicación — ¿Qué se puede publicar?
- **15.17** Riesgos para participantes — ¿Qué riesgos corren los participantes?
- **15.18** Escalamiento de incidentes — ¿Cómo se escalan incidentes éticos?
- **15.19** Aprobaciones requeridas — ¿Qué aprobaciones éticas o legales se requieren?
- **15.20** Acciones prohibidas — ¿Qué está prohibido hacer?

### Fase 16 · Cronograma, recursos y presupuesto
*Regla: no inventes precios. Sin tarifas, construye la estructura de costos y deja los valores como `[PENDIENTE]`.*

- **16.1** ★ Fecha de inicio — ¿Cuándo inicia?
- **16.2** ★ Fecha límite — ¿Cuándo termina?
- **16.3** Hitos — ¿Qué hitos tiene?
- **16.4** Duración por fase — ¿Cuánto dura cada fase?
- **16.5** Dependencias — ¿Qué dependencias de tiempo hay?
- **16.6** ★ Equipo disponible — ¿Qué equipo hay?
- **16.7** Proveedores — ¿Qué proveedores se contratan?
- **16.8** Herramientas — ¿Qué herramientas se usan?
- **16.9** ★ Presupuesto — ¿Cuál es el presupuesto?

*16.10-16.15 se entregan como una sola tabla de costos: el agente arma las filas y el usuario pone los valores.*

- **16.10** Incentivos — ¿Cuánto cuestan los incentivos?
- **16.11** Viajes — ¿Hay viajes?
- **16.12** Plataformas — ¿Qué cuestan las plataformas?
- **16.13** Transcripción — ¿Qué cuesta la transcripción?
- **16.14** Análisis — ¿Qué cuesta el análisis?
- **16.15** Diseño de entregables — ¿Qué cuesta el diseño de entregables?
- **16.16** Contingencia — ¿Qué reserva de contingencia hay?
- **16.17** Restricciones críticas — ¿Qué restricciones de recursos son críticas?
- **16.18** Escenarios — ¿Cómo se ven los escenarios mínimo, recomendado y ampliado?

### Fase 17 · Entregables y activación
*Regla: toda recomendación debe enlazar evidencia, insight de origen, acción posible, responsable, indicador y resultado esperado.*

- **17.1** Entregables obligatorios — ¿Qué entregables son obligatorios?
- **17.2** Audiencia por entregable — ¿Para quién es cada uno?
- **17.3** Formato — ¿En qué formato?
- **17.4** Nivel de detalle — ¿Con qué nivel de detalle?
- **17.5** Visualizaciones — ¿Qué visualizaciones incluyen?
- **17.6** Presentación — ¿Cómo se presentan?
- **17.7** ★ Taller de activación — ¿Habrá taller de activación?
- **17.8** Registro de recomendaciones — ¿Cómo se registran las recomendaciones?
- **17.9** ★ Responsables de acciones — ¿Quién ejecuta cada acción?
- **17.10** Indicadores — ¿Con qué indicadores se mide?
- **17.11** Línea base — ¿Cuál es la línea base?
- **17.12** ★ Metas — ¿Qué metas se fijan?
- **17.13** Seguimiento — ¿Cómo se hace seguimiento?
- **17.14** Medición de resultados — ¿Cómo se miden los resultados?
- **17.15** Aprendizajes reutilizables — ¿Qué aprendizajes se pueden reutilizar?

### Fase 18 · Riesgos y limitaciones
*El agente arma un registro de riesgos: 18.1-18.12 son las filas; 18.13-18.18 son sus columnas (probabilidad, impacto, mitigación, responsable, señal y contingencia). Se entrega como una tabla en uno o dos lotes.*

- **18.1** Riesgos metodológicos — ¿Qué riesgos metodológicos hay?
- **18.2** Riesgos de reclutamiento — ¿Y de reclutamiento?
- **18.3** Riesgos de sesgo — ¿Y de sesgo?
- **18.4** Riesgos de cobertura — ¿Y de cobertura?
- **18.5** Riesgos de privacidad — ¿Y de privacidad?
- **18.6** Riesgos operativos — ¿Y operativos?
- **18.7** Riesgos tecnológicos — ¿Y tecnológicos?
- **18.8** Riesgos presupuestales — ¿Y presupuestales?
- **18.9** Riesgos de tiempo — ¿Y de tiempo?
- **18.10** Riesgos de adopción — ¿Y de adopción de resultados?
- **18.11** Riesgos reputacionales — ¿Y reputacionales?
- **18.12** Limitaciones inevitables — ¿Qué limitaciones son inevitables?
- **18.13** Probabilidad — ¿Qué probabilidad tiene cada riesgo?
- **18.14** Impacto — ¿Qué impacto tendría?
- **18.15** Mitigación — ¿Cómo se mitiga?
- **18.16** ★ Responsable — ¿Quién lo vigila?
- **18.17** Señal de alerta — ¿Qué señal anticipa que ocurrirá?
- **18.18** Plan de contingencia — ¿Qué se hace si ocurre?

> **→ Gate G3 · Preparación para campo** (ver *Gates*).

---

## BLOQUE 7 · CIERRE (Fases 19-20)

### Fase 19 · Auditoría metodológica
*Revisiones separadas. Clasifica cada defecto: **Crítico** (impide aprobar) · **Alto** (corregir antes de campo) · **Medio** (ajuste documentado) · **Bajo** (mejora deseable) · **Observación**. La hace el agente; propone la corrección de cada defecto crítico y alto en un lote.*

- **19.1** Coherencia con la decisión — ¿El diseño responde a la decisión?
- **19.2** Claridad del problema — ¿El problema está claro?
- **19.3** Calidad de objetivos — ¿Los objetivos son sólidos?
- **19.4** Calidad de preguntas — ¿Las preguntas son sólidas?
- **19.5** Adecuación metodológica — ¿El método es adecuado?
- **19.6** Justificación de muestra — ¿La muestra está justificada?
- **19.7** Cobertura instrumental — ¿Los instrumentos cubren todo?
- **19.8** Viabilidad operativa — ¿Es viable operativamente?
- **19.9** Plan analítico — ¿El plan de análisis es sólido?
- **19.10** Trazabilidad — ¿La trazabilidad está completa?
- **19.11** Contradicciones — ¿Quedan contradicciones abiertas?
- **19.12** Ética y privacidad — ¿Ética y privacidad están resueltas?
- **19.13** Presupuesto — ¿El presupuesto es coherente?
- **19.14** Cronograma — ¿El cronograma es viable?
- **19.15** Riesgos — ¿Los riesgos tienen mitigación?
- **19.16** Aprobaciones — ¿Están todas las aprobaciones?

### Fase 20 · Field-Ready Research Package

- **20.1** Documento final generado — ¿Está generado el paquete completo?
- **20.2** Revisión adversarial — ¿Pasó la revisión adversarial sin defectos críticos?
- **20.3** ★ Entrega aprobada — ¿El usuario aprueba el paquete?

**Fuentes (obligatorio, en este orden):** (1) `DASHBOARD.md` (respuesta vigente de cada ítem y gates); (2) `INSTRUMENTOS.md` (texto de los instrumentos); (3) `BITACORA.md` (detalle y origen de cada decisión); (4) la evidencia del proyecto (p. ej. *Evidence Map*) para argumentos y cifras.

**Honestidad documental:** todo ítem `[ ]`, `[p]` o `[r]` → `⚠️ [estado] — pendiente de confirmación`. Ítem aprobado sin detalle en la bitácora → `⚠️ Aprobado sin detalle en bitácora`.

**Estructura del paquete (35 secciones):** 1 Portada · 2 Control de versión · 3 Resumen ejecutivo · 4 Decision Case · 5 Contexto · 6 Problema empresarial · 7 Problema de decisión · 8 Problema de investigación · 9 Objetivos · 10 Preguntas · 11 Hipótesis y supuestos · 12 Alcance y exclusiones · 13 Audiencias · 14 Evidencia requerida · 15 Diseño metodológico · 16 Población y muestra · 17 Técnicas · 18 Instrumentos · 19 Matriz de trazabilidad · 20 Plan de reclutamiento · 21 Plan de campo · 22 Plan de análisis · 23 Ética y privacidad · 24 Cronograma · 25 Presupuesto · 26 Roles y responsabilidades · 27 Riesgos y mitigaciones · 28 Entregables · 29 Plan de activación · 30 Indicadores de resultado · 31 Limitaciones · 32 Registro de aprobaciones · 33 Historial de cambios · 34 Lista de verificación para iniciar campo · 35 Anexos.

**Revisión final adversarial (antes de presentar):** ¿Qué afirmaciones no tienen soporte? · ¿Qué objetivos están poco cubiertos? · ¿Qué preguntas no tienen método? · ¿Qué instrumentos tienen preguntas innecesarias? · ¿Qué segmentos están subrepresentados? · ¿Qué supuestos se tratan como hechos? · ¿Qué contradicciones siguen abiertas? · ¿Qué sesgos introduce el diseño? · ¿Qué riesgos no tienen mitigación? · ¿Qué componentes no tienen responsable? · ¿Qué acciones no tienen indicador? · ¿Qué requiere aprobación humana? · ¿Se puede explicar el origen de cada decisión metodológica? · ¿Hay algún defecto crítico que impida iniciar campo? → Si hay un defecto crítico, no declares el paquete listo: vuelve al componente y resuélvelo en un lote de corrección.

**Entrega:** entrega el paquete como documento (`Entregable Final - [Nombre].md`, o en el formato que pida el usuario), marca 20.1-20.3 y el gate *Entrega final* en `DASHBOARD.md`, y pregunta:
*"¿Apruebas el Field-Ready Research Package para iniciar trabajo de campo?"*

---

## Gates

| Gate | Momento | No se aprueba si falta… |
|---|---|---|
| **G0 · Admisión** | Tras Fase 1 | Necesidad real · decisión potencialmente identificable · propietario o responsable · razón para investigar · viabilidad mínima · permiso para procesar información · ausencia de riesgos inaceptables |
| **G1 · Definición** | Tras Fase 6 | Problema formulado · decisión y propietario · incertidumbre crítica · restricciones · alcance y exclusiones · audiencias · objetivos auditados · preguntas, hipótesis y supuestos · explicaciones alternativas y evidencia a favor/en contra |
| **G2 · Diseño** | Tras Fase 13 | Evidencia requerida definida · coherencia objetivos-métodos · muestra justificada · cobertura instrumental · trazabilidad sin brechas · plan analítico · riesgos y consentimientos aplicables identificados · aprobación humana |
| **G3 · Preparación para campo** | Tras Fase 18 | Instrumentos aprobados · materiales completos · versiones congeladas · responsables · permisos · riesgos mitigados · cronograma viable · paquete exportable · protocolo de calidad · plan de manejo de incidentes |
| **Entrega final** | Tras Fase 20 | Auditoría sin defectos críticos ni altos abiertos · paquete generado · revisión adversarial · aprobación del usuario |

---

## Resumen de conteo

| Bloque | Fases | Ítems |
|---|---|---|
| 1 · Inicio y Admisión | 0-2 | 35 |
| 2 · Enmarcado | 3-4 | 30 |
| 3 · Conocimiento | 5-6 | 18 |
| 4 · Diseño Metodológico | 7-11 | 67 |
| 5 · Trazabilidad y Análisis | 12-13 | 29 |
| 6 · Operación de Campo | 14-18 | 91 |
| 7 · Cierre | 19-20 | 19 |
| **Total** | **0-20** | **289** |

Los criterios de gate se verifican aparte y no suman al porcentaje de avance. **Núcleo ★:** 63 ítems (B1 19 · B2 10 · B3 3 · B4 8 · B5 3 · B6 19 · B7 1).
