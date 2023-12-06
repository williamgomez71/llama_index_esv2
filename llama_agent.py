
from llama_index_spanish import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
    VectorStoreIndex,
    ListIndex,
    SummaryIndex
)
from typing import  List
from llama_index_spanish.tools.function_tool import FunctionTool
import re
from robin_index import RobinManageIndex
from llama_index_spanish.tools import QueryEngineTool, ToolMetadata
from llama_index_spanish.agent import ReActAgent
from robin_llm import RobinLLM
from bs4 import BeautifulSoup
""" march_2022 = SimpleDirectoryReader(input_files=["../data/10q/uber_10q_march_2022.pdf"]).load_data()
june_2022 = SimpleDirectoryReader(input_files=["../data/10q/uber_10q_june_2022.pdf"]).load_data()
sept_2022 = SimpleDirectoryReader(input_files=["../data/10q/uber_10q_sept_2022.pdf"]).load_data() """

march_2022 = "./xuberdocs/1/"
june_2022 = "./xuberdocs/2/"
sept_2022 = "./xuberdocs/3/"
""" march_2022 = "./xuberdocs/1/Uber-Q1-23-Earnings.pdf"
june_2022 = "./xuberdocs/2/Uber-Q3-22-Earnings.pdf"
sept_2022 = "./xuberdocs/3/Uber-Q4-22-Earnings.pdf" """
march_2022i = "./xuberdocs/index/1i/"
march_2022isummary = "./xuberdocs/index/1isummary/"
june_2022i = "./xuberdocs/index/2i/"
sept_2022i = "./xuberdocs/index/3i/"

#vector_index = base_index.create_vector_index("liceo_vector-multilingual-e5-large2")

base_index = RobinManageIndex( path_docs = march_2022)
""" march_index =base_index.create_vector_index(march_2022i)

base_index = RobinManageIndex( path_docs = june_2022)
june_index = base_index.create_vector_index(june_2022i)

base_index = RobinManageIndex( path_docs = sept_2022)
sept_index = base_index.create_vector_index(sept_2022i) """

march_index = base_index.load_persistent_index(march_2022i)
june_index = base_index.load_persistent_index(june_2022i)
sept_index = base_index.load_persistent_index(sept_2022i)
#base_index.create_document_summary_document_index(march_2022isummary)
march_2022isummary_index = base_index.load_persistent_index(march_2022isummary)


""" print(march_2022isummary_index.get_document_summary("Uber-Q1-23-Earnings.pdf"))
print(march_2022isummary_index.get_document_summary("Uber-Q1-23-Earnings.pdf")) """
""" print(dir(march_2022isummary_index))
print(march_2022isummary_index.as_retriever().retrieve("give me a summary of the page 9")) """


def get_summary_by_page(
    page = None
) -> List:
    """Retrieve nodes."""
    summary_ids = march_2022isummary_index._index_struct.summary_ids
    summaries = []
    for idx in summary_ids:
        summary_text = march_2022isummary_index.docstore.get_node(idx).get_content()
        summary_id = march_2022isummary_index._index_struct.summary_id_to_node_ids[idx]
        summary_nodes_id = march_2022isummary_index.docstore.get_nodes(summary_id)
        if page != None:
            for node in summary_nodes_id:
                if node.metadata.get('page_label') == str(page):
                    summaries.append({"summary_text": summary_text, "page": node.metadata.get('page_label')})
        else:
            for node in summary_nodes_id:
                summaries.append({"summary_text": summary_text, "page": node.metadata.get('page_label')})

    seen = set()
    # Filtrar el array para eliminar duplicados
    array_filtrado = []
    for item in summaries:
        # Crear una tupla con el texto y el número de página
        id = (item['summary_text'], item['page'])

        # Si esta combinación no se ha visto antes, añádela al array filtrado
        if id not in seen:
            array_filtrado.append(item)
            seen.add(id)
    return array_filtrado

print(get_summary_by_page(3))






# define query engine
q1_23 = march_index.as_query_engine(similarity_top_k=3)
q3_22 = june_index.as_query_engine(similarity_top_k=3)
q4_22 = sept_index.as_query_engine(similarity_top_k=3)


llm = RobinLLM()
query_engine_tools = [
    QueryEngineTool(
        query_engine=q1_23,
        metadata=ToolMetadata(
            name="uber_q1_2023",
            description=(
                "Provides information about UBER financials quarter 1 for year 2023. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=q3_22,
        metadata=ToolMetadata(
            name="uber_q3_2022",
            description=(
                "Provides information about UBER financials quarter 3 for year 2022.  "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    
    QueryEngineTool(
        query_engine=q4_22,
        metadata=ToolMetadata(
            name="uber_q4_2022",
            description=(
                "Provides information about UBER financials quarter 4 for year 2022. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
]

import requests

def search_internet(url: str) -> str:
    """
    Use this tool if you need to search in internet for information that you don't know.
    """
    respuesta = requests.get(url)
    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        # Contenido de la página web
        contenido = respuesta.text
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        # Extraer solo el texto de la página
        texto = soup.get_text(separator='\n')
    else:
        print("Error al descargar la página web")
        # Opcionalmente, puedes guardar el contenido en un archivo
    patron = r"\n+"
    # Reemplazamos todos los saltos de línea consecutivos con un solo salto de línea
    texto = re.sub(patron, "\n", texto)
    # Opcionalmente, puedes guardar el contenido en un archivo
    with open("pagina_web.html", "w", encoding="utf-8") as archivo:
        archivo.write(texto)
    return texto


def qa_general_questions(question: str) -> str:
    """
    Use this tool if you need to search in internet for information that you don't know.
    """
    with open('logging2.txt', 'a') as archivo:
        # Escribe una línea de texto
        archivo.write(f"-------------------answer----------------------------------------------------------------------\n")
        archivo.write("general questions\n")
    return ["no tengo informacion suficiente para responder tu pregunta, me puedes indicar si necesitas resumen de la pagina o de todo el documento?", False]
    return question


def summary_information(page = None)-> str:
    """
Use esta herramienta si el usuario solicita algun tipo de resumen de un texto o de una pagina especifica del documento.
    """
    print(page)
    print(page)
    print(page)
    print(page)
    print(page)
    with open('logging2.txt', 'a') as archivo:
        # Escribe una línea de texto
        archivo.write(f"-------------------answer----------------------------------------------------------------------\n")
        archivo.write("summary\n")
    return ["no tengo informacion suficiente para responder tu pregunta, me puedes indicar si necesitas resumen de la pagina o de todo el documento?", False]
    return """ 
En el año 1934, en una vieja casa de la calle 12 No. 3-62, funda el Dr. Jesús Cásas Manrique un pequeño Colegio con el nombre de LICEO DE LA INFANCIA, contando con el reducido número de 34 estudiantes.

Los alumnos van en aumento, e incapaz la casa para recibir más, al cabo de dos años consigue el Dr. Casas la Quinta "Aranjuez, situada en la carrera 13 No. 56-16. El nombre primitivo cambia por LICEO DE CERVANTES, se dice que inspirado por el padre del fundador, José Joaquín Casas Castañeda, destacado literato, poeta, admirador de Cervantes con su Quijote, pues se dice que estando en España de Embajador por los años 1930, hizo a pie la ruta del Quijote. El, que había sido ministro de Educación, honró el Liceo siendo uno de sus profesores.

En el año 1941 se gradúan los primeros Bachilleres, que suman 9.

La nueva sede se inaugura en 1944, edificio construido para colegio, de estilo Clásico Español.

Ante el futuro incierto del Cervantes que su propietario y Director preveía, en vista de que ninguno de sus hijos se inclinaba por la enseñanza, se decidió a venderlo, de preferencia a una Comunidad Religiosa. La de los Agustinos va a ser la que lo va a conseguir, comprometiéndose en cumplir la condición deseada por el Dr. Jesús Casas de que se conserve el nombre.

"""


#function_tool = FunctionTool.from_defaults(fn=search_internet,description="Utilice esta herramienta si necesita buscar en Internet información que no conoce. Por ejemplo si el usuario indica: dame informacion de este sitio http://example.com deberas usar este herramienta antes de dar la respuesta. Si el usuario no indica una url en la pregunta es mejor usar la siguiente herramienta y no esta.")
function_tool = FunctionTool.from_defaults(fn=qa_general_questions, description="""Esta herramienta es para responder preguntas generales o especificas de un documento. No sirve para generar resumenes
         A contiacion algunos ejemplos de preguntas que se pueden usar con esta herramienta:                                  
        "Cómo puedo cambiar la contraseña de mi correo electrónico?"
        "Qué ingredientes necesito para hacer una lasaña?"
        "Cuál es la capital de Francia?"
        "Cómo se calcula el área de un círculo?"
        "Qué ejercicios son buenos para la espalda baja?"
        "Que es la vida?"
        use la pregunta del usuario como entrada para esta herramienta.
        """)
function_tool2 = FunctionTool.from_defaults(fn=summary_information, description="Utilice esta herramienta si el usuario solicita algun tipo de resumen o sumarizacion de un texto o de una pagina especifica de un documento. Esta herramienta puede generar resumenes de cualquier cosa. si el usuario solicita un resumen debes usar esta herramienta" )

tools = [function_tool, function_tool2]


agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, max_iterations=2)

#response = agent.chat("What was Uber's revenue growth in 2022?")
#response = agent.chat("add 5  more  8998")
#response = agent.chat("what is the current president in Colombia")
#response = agent.chat("dame un resumen de la siguiente pagina https://www.liceocervantes.edu.co/index.php/nuestro-liceo/historia")
#response = agent.chat("en orden cronologico dame los puntos mas relevantes de la informacion de esta pagina https://www.liceocervantes.edu.co/index.php/nuestro-liceo/historia")
#response = agent.chat("Cómo puedo cambiar la contraseña de mi correo electrónico??")
#response = agent.chat("tienes un resumen de la pagina del documento")

agent2 = ReActAgent.from_tools(tools, llm=llm, verbose=True, max_iterations=2)
value = """human: tienes un resumen del documento en la pagina ?
assintant: no tengo informacion suficiente para responder tu pregunta, me puedes indicar si necesitas resumen de la pagina o de todo el documento?
human: pagina 33
"""
#response = agent2.chat(value)
#print(str(response))


preguntas = [
    # Enviar email
    "Escribe un correo para confirmar la reunión de mañana.",
    "Notifica a los clientes sobre la actualización de nuestro producto.",
    "Envía una invitación para el evento de caridad de este fin de semana.",
    "Remite el informe de ventas a la gerencia.",
    "Informa al equipo sobre el cambio en la política de vacaciones.",
    # Preguntas generales
    "Cómo puedo cambiar la contraseña de mi correo electrónico?",
    "que es la vida?",
    "de que se trata la vida?",
    "tienes un resumen de la pagina del documento",
    "¿Qué ingredientes necesito para hacer una lasaña?",
    "¿Cuál es la capital de Francia?",
    "¿Cómo se calcula el área de un círculo?",
    "¿Qué ejercicios son buenos para la espalda baja?",
    # Buscar por internet
    "Encuentra un buen restaurante italiano cerca de mí.",
    "Busca las últimas noticias sobre el cambio climático.",
    "Necesito información sobre los mejores teléfonos inteligentes de 2023.",
    "¿Cuáles son los estrenos de cine de esta semana?",
    "Busca cursos en línea para aprender programación.",
    # Generar resumen
    "Haz un resumen del último informe de mercado financiero.",
    "Necesito un resumen del libro 'El Principito'.",
    "Resume las características principales de la Revolución Industrial.",
    "Por favor, resume las noticias principales de hoy.",
    "Elabora un resumen ejecutivo de la reunión de ayer."
]


for question in  preguntas:
    agent2 = ReActAgent.from_tools(tools, llm=llm, verbose=False, max_iterations=2)
    response = agent2.chat(question)
