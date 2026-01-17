import gradio as gr
from google import genai
import random
import time
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("La variable de entorno GEMINI_API_KEY no está definida")

client = genai.Client(api_key=GEMINI_API_KEY)

TEMAS_ALEATORIOS = {
    "ES": [
        "Inteligencia Artificial",
        "Psicología humana",
        "Dinero y riqueza",
        "Hábitos de las personas exitosas",
        "Historia poco conocida",
        "Curiosidades científicas",
        "Productividad",
        "Errores comunes en la vida",
        "Tecnología del futuro",
        "Cerebro humano",
        "Recetas de cocina",
        "Comandos de git",
        "Frases de éxito",
        "Animales curiosos",
        "Felicidad humana",
        "Conseguir el amor"
    ],
    "EN": [
        "Artificial Intelligence",
        "Human Psychology",
        "Money and Wealth",
        "Habits of Successful People",
        "Unknown History",
        "Scientific Curiosities",
        "Productivity",
        "Common Life Mistakes",
        "Future Technology",
        "Human Brain",
        "Cooking Recipes",
        "Git Commands",
        "Success Quotes",
        "Curious Animals",
        "Human Happiness",
        "Finding Love"
    ]
}

TRADUCCIONES = {
    "ES": {
        "titulo": "# X Viral Growth AI",
        "subtitulo": "Genera hilos y tweets diseñados para maximizar **engagement en X (Twitter)**.",
        "label_tema": "¿De qué quieres hablar?",
        "placeholder_tema": "Ej: Recetas de cocina, comandos de git...",
        "label_tipo": "Selecciona el tipo de contenido que quieres generar",
        "label_hashtags": "Añadir hashtags al final del tweet",
        "btn_generar": "Generar Contenido",
        "btn_random": "🎲 Generar Tweet Aleatorio",
        "label_output": "Tu contenido para Twitter (X)",
        "footer": 'Publica directamente en <a href="https://x.com" target="_blank"><strong>x.com</strong></a>',
        "tipos": ["Hilo Viral", "Dato Curioso", "Historia/Storytelling", "Explicación (EL5)"]
    },
    "EN": {
        "titulo": "# X Viral Growth AI",
        "subtitulo": "Generate threads and tweets designed to maximize **engagement on X (Twitter)**.",
        "label_tema": "What do you want to talk about?",
        "placeholder_tema": "E.g.: Cooking recipes, git commands...",
        "label_tipo": "Select the type of content you want to generate",
        "label_hashtags": "Add hashtags at the end of the tweet",
        "btn_generar": "Generate Content",
        "btn_random": "🎲 Generate Random Tweet",
        "label_output": "Your content for Twitter (X)",
        "footer": 'Post directly on <a href="https://x.com" target="_blank"><strong>x.com</strong></a>',
        "tipos": ["Viral Thread", "Fun Fact", "Storytelling", "ELI5 Explanation"]
    }
}

def generar_twitter(tema, tipo_post, usar_hashtags, idioma):
    if idioma == "ES":
        estilos = {
            "Hilo Viral": "Crea un hilo de 5 tweets. El primero debe tener un gancho (hook) increíble que genere curiosidad.",
            "Dato Curioso": "Escribe un solo tweet impactante sobre un dato que nadie sepa del tema. Debe empezar con '¿Sabías que...?'",
            "Historia/Storytelling": "Escribe un tweet que cuente una breve lección o historia personal sobre el tema para conectar emocionalmente.",
            "Explicación (EL5)": "Explica el tema como si tuviera 5 años, de forma sencilla y clara en un solo tweet."
        }
        regla_hashtags = "- Usa máximo 2-3 hashtags relevantes." if usar_hashtags else "- No uses ningún hashtag."
        
        instruccion = f"""
        Eres un experto en crecimiento en Twitter (X). 
        Tu objetivo es crear contenido sobre: '{tema}'.
        Formato solicitado: {estilos[tipo_post]}
        
        IMPORTANTE: Genera TODO el contenido en ESPAÑOL.
        
        Reglas:
        - No uses lenguaje aburrido.
        {regla_hashtags}
        - Mantén cada tweet bajo el límite de caracteres (280).
        - Emplea un lenguaje humano, cercano y natural, que conecte con la audiencia.
        - Evita repeticiones y frases hechas.
        - Suena lo mas humano posible, que sea dificil de detectar que ha sido generado por una IA.
        - Evita el uso de emojis.
        - Solo genera como respuesta el tweet, sin ningun otro texto.
        - Si el tweet es un hilo, poner ---- como separador entre tweets. (y 1/5, 2/5, etc)
        - Si el tweet es un hilo, poner "Abro hilo: " al al final del primer tweet.
        - Si el tweet es un hilo, poner solo los hashtags en el ultimo tweet (en caso de que una de las reglas sea incluir hashtags).
        """
    else:
        estilos = {
            "Viral Thread": "Create a thread of 5 tweets. The first one must have an incredible hook that generates curiosity.",
            "Fun Fact": "Write a single impactful tweet about a fact nobody knows about the topic. Start with 'Did you know...?'",
            "Storytelling": "Write a tweet that tells a brief lesson or personal story about the topic to connect emotionally.",
            "ELI5 Explanation": "Explain the topic as if the reader were 5 years old, in a simple and clear way in a single tweet."
        }
        regla_hashtags = "- Use a maximum of 2-3 relevant hashtags." if usar_hashtags else "- Do not use any hashtags."
        
        instruccion = f"""
        You are an expert in Twitter (X) growth. 
        Your goal is to create content about: '{tema}'.
        Requested format: {estilos[tipo_post]}
        
        IMPORTANT: Generate ALL content in ENGLISH.
        
        Rules:
        - Don't use boring language.
        {regla_hashtags}
        - Keep each tweet under the character limit.
        - Use human, close and natural language that connects with the audience.
        - Avoid repetitions and clichés.
        - Sound as human as possible, make it difficult to detect it was AI-generated.
        - Avoid using emojis.
        - Only generate the tweet as a response, with no other text.
        - If it's a thread, use ---- as separator between tweets. (and 1/5, 2/5, etc)
        - If it's a thread, put only the hashtags in the last tweet (in case one of the rules is to include hashtags).
        """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=instruccion
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return "API limit exceeded. Wait a few minutes" if idioma == "EN" else "Límite de API excedido. Espera unos minutos"
        return f"Error: {error_msg}"

def generar_twitter_aleatorio(tipo_post, usar_hashtags, idioma):
    tema_random = random.choice(TEMAS_ALEATORIOS[idioma])
    return generar_twitter(tema_random, tipo_post, usar_hashtags, idioma)

def cambiar_idioma(idioma):
    t = TRADUCCIONES[idioma]
    return (
        gr.update(value=t["titulo"]),
        gr.update(value=t["subtitulo"]),
        gr.update(label=t["label_tema"], placeholder=t["placeholder_tema"]),
        gr.update(choices=t["tipos"], label=t["label_tipo"], value=t["tipos"][0]),
        gr.update(label=t["label_hashtags"]),
        gr.update(value=t["btn_generar"]),
        gr.update(value=t["btn_random"]),
        gr.update(label=t["label_output"]),
        gr.update(value=f'<div id="footer-link">{t["footer"]}</div>')
    )

css = """
body {
    background-color: #f9f9f9;
}

#language-selector {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

#btn-generar {
    background-color: #333 !important;
    color: white !important;
}

#btn-generar:hover {
    background-color: #555 !important;
}

#footer-link {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
}

#radio-tipo input[type="radio"]:checked {
    accent-color: #333 !important;
    background-color: #333 !important;
    border-color: #333 !important;
    color: white !important;
}

#input-tema textarea:focus,
#input-tema input:focus {
    border-color: #333 !important;
    box-shadow: 0 0 0 1px #333 !important;
}

#checkbox-hashtags input[type="checkbox"]:checked {
    accent-color: #333 !important;
    background-color: #333 !important;
    border-color: #333 !important;
    color: white !important;
}

#checkbox-hashtags input[type="checkbox"] {
    accent-color: #333 !important;
    border-color: #333 !important;
    color: white !important;
}

#language-selector input[type="radio"]:checked {
    accent-color: #333 !important;
    background-color: #333 !important;
    border-color: #333 !important;
    color: white !important;
}


"""

with gr.Blocks(css=css, title="X Viral Growth AI") as demo:
    idioma_state = gr.State("ES")
    
    with gr.Row():
        with gr.Column(scale=10):
            pass
        with gr.Column(scale=1, min_width=100):
            selector_idioma = gr.Radio(
                choices=["ES", "EN"],
                value="ES",
                label="Language",
                elem_id="language-selector"
            )
    
    titulo_md = gr.Markdown("# X Viral Growth AI")
    subtitulo_md = gr.Markdown(
        "Genera hilos y tweets diseñados para maximizar **engagement en X (Twitter)**."
    )

    with gr.Row():
        with gr.Column():
            input_tema = gr.Textbox(
                label="¿De qué quieres hablar?",
                placeholder="Ej: Recetas de cocina, comandos de git...",
                elem_id="input-tema"
            )

            input_tipo = gr.Radio(
                choices=["Hilo Viral", "Dato Curioso", "Historia/Storytelling", "Explicación (EL5)"],
                label="Selecciona el tipo de contenido que quieres generar",
                value="Hilo Viral",
                elem_id="radio-tipo"
            )

            add_hashtags = gr.Checkbox(
                label="Añadir hashtags al final del tweet",
                value=True,
                elem_id="checkbox-hashtags"
            )
            btn_generar = gr.Button("Generar Contenido", variant="primary", elem_id="btn-generar")
            btn_random = gr.Button("🎲 Generar Tweet Aleatorio")

        with gr.Column():
            output_text = gr.Textbox(
                label="Tu contenido para Twitter (X)",
                lines=15
            )

    footer_md = gr.HTML(
        """
        <div id="footer-link">
            Publica directamente en  
            <a href="https://x.com" target="_blank"><strong>x.com</strong></a>
        </div>
        """
    )

    selector_idioma.change(
        fn=cambiar_idioma,
        inputs=[selector_idioma],
        outputs=[titulo_md, subtitulo_md, input_tema, input_tipo, add_hashtags, btn_generar, btn_random, output_text, footer_md]
    ).then(
        fn=lambda x: x,
        inputs=[selector_idioma],
        outputs=[idioma_state]
    )

    btn_generar.click(
        fn=generar_twitter,
        inputs=[input_tema, input_tipo, add_hashtags, idioma_state],
        outputs=output_text
    )

    btn_random.click(
        fn=generar_twitter_aleatorio,
        inputs=[input_tipo, add_hashtags, idioma_state],
        outputs=output_text
    )

demo.launch(
    favicon_path="favicon.png"
)