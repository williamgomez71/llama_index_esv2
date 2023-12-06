"""Set of default prompts."""

from llama_index_spanish.prompts.base import PromptTemplate
from llama_index_spanish.prompts.prompt_type import PromptType

############################################
# Tree
############################################

DEFAULT_SUMMARY_PROMPT_TMPL = (
    "Escribe un resumen de lo siguiente. Intente utilizar sólo el"
    "información proporcionada."
    "Intente incluir tantos detalles clave como sea posible.\n"
    "\n"
    "\n"
    "{context_str}\n"
    "\n"
    "\n"
    'RESUMEN:"""\n'
)

DEFAULT_SUMMARY_PROMPT = PromptTemplate(
    DEFAULT_SUMMARY_PROMPT_TMPL, prompt_type=PromptType.SUMMARY
)

# insert prompts
DEFAULT_INSERT_PROMPT_TMPL = (
    "La información de contexto se encuentra a continuación. Se proporciona en una lista numerada. "
    "(1 a {num_chunks}), "
    "donde cada elemento de la lista corresponde a un resumen.\n"
    "---------------------\n"
    "{context_list}"
    "---------------------\n"
    "Dada la información del contexto, aquí hay una nueva pieza de "
    "información: {new_chunk_text}\n"
    "Responda con el número correspondiente al resumen que debe actualizarse. "
    "La respuesta debe ser el número correspondiente a la "
    "resumen que sea más relevante para la pregunta.\n"
)
DEFAULT_INSERT_PROMPT = PromptTemplate(
    DEFAULT_INSERT_PROMPT_TMPL, prompt_type=PromptType.TREE_INSERT
)


# # single choice
DEFAULT_QUERY_PROMPT_TMPL = (
    "Algunas opciones se dan a continuación. Se proporciona en una lista numerada."
    "(1 a {num_chunks}), "
    "donde cada elemento de la lista corresponde a un resumen.\n"
    "---------------------\n"
    "{context_list}"
    "\n---------------------\n"
    "Usando sólo las opciones anteriores y sin conocimientos previos, regrese"
    "la elección que es más relevante para la pregunta:'{query_str}'\n"
    "Proporcione opciones en el siguiente formato: 'RESPUESTA: <número>' y explique por qué "
    "Este resumen fue seleccionado en relación con la pregunta.\n"
)
DEFAULT_QUERY_PROMPT = PromptTemplate(
    DEFAULT_QUERY_PROMPT_TMPL, prompt_type=PromptType.TREE_SELECT
)

# multiple choice
DEFAULT_QUERY_PROMPT_MULTIPLE_TMPL = (
    "Algunas opciones se dan a continuación. Se proporciona en un número"
    "lista (1 a {num_chunks}), "
    "donde cada elemento de la lista corresponde a un resumen.\n"
    "---------------------\n"
    "{context_list}"
    "\n---------------------\n"
    "Utilizando sólo las opciones anteriores y sin conocimientos previos, devuelva las mejores opciones "
    "(no más de  {branching_factor}, clasificados del más relevante al menos) que"
    "Son los más relevantes para la pregunta:'{query_str}'\n"
    "Proporcione opciones en el siguiente formato: 'RESPUESTA: <números>' y explique por qué"
    "Estos resúmenes fueron seleccionados en relación con la pregunta.\n"
)
DEFAULT_QUERY_PROMPT_MULTIPLE = PromptTemplate(
    DEFAULT_QUERY_PROMPT_MULTIPLE_TMPL, prompt_type=PromptType.TREE_SELECT_MULTIPLE
)


DEFAULT_REFINE_PROMPT_TMPL = (
    "La consulta original es la siguiente: {query_str}\n"
    "Hemos proporcionado una respuesta existente: {existing_answer}\n"
    "Tenemos la oportunidad de refinar la respuesta existente."
    "(solo si es necesario) con más contexto a continuación.\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "Dado el nuevo contexto, refine la respuesta original para mejorarla. "
    "responder la consulta."
    "Si el contexto no es útil, devuelva la respuesta original.\n"
    "Respuesta refinada:"
)
DEFAULT_REFINE_PROMPT = PromptTemplate(
    DEFAULT_REFINE_PROMPT_TMPL, prompt_type=PromptType.REFINE
)


DEFAULT_TEXT_QA_PROMPT_TMPL = (
    "La información de contexto se encuentra a continuación.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Dada la información del contexto y no el conocimiento previo,"
    "responder la consulta.\n"
    "Consulta: {query_str}\n"
    "Respuesta:"
)
DEFAULT_TEXT_QA_PROMPT = PromptTemplate(
    DEFAULT_TEXT_QA_PROMPT_TMPL, prompt_type=PromptType.QUESTION_ANSWER
)

DEFAULT_TREE_SUMMARIZE_TMPL = (
    "La información contextual de múltiples fuentes se encuentra a continuación.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Dada la información de múltiples fuentes y no el conocimiento previo, "
    "responder la consulta.\n"
    "Consulta: {query_str}\n"
    "Respuesta: "
)
DEFAULT_TREE_SUMMARIZE_PROMPT = PromptTemplate(
    DEFAULT_TREE_SUMMARIZE_TMPL, prompt_type=PromptType.SUMMARY
)


############################################
# Keyword Table
############################################

DEFAULT_KEYWORD_EXTRACT_TEMPLATE_TMPL = (
    "A continuación se proporciona algo de texto. Dado el texto, extraiga hasta {max_keywords} "
    "palabras clave del texto. Evite las palabras vacías."
    "---------------------\n"
    "{text}\n"
    "---------------------\n"
    "Proporcione palabras clave en el siguiente formato separado por comas: 'PALABRAS CLAVE: <palabras clave>'\n"
)
DEFAULT_KEYWORD_EXTRACT_TEMPLATE = PromptTemplate(
    DEFAULT_KEYWORD_EXTRACT_TEMPLATE_TMPL, prompt_type=PromptType.KEYWORD_EXTRACT
)


# NOTE: the keyword extraction for queries can be the same as
# the one used to build the index, but here we tune it to see if performance is better.
DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE_TMPL = (
    "A continuación se proporciona una pregunta. Dada la pregunta, extraiga hasta{max_keywords} "
    "palabras clave del texto. Centrarse en extraer las palabras clave que podemos utilizar "
    "para buscar mejores respuestas a la pregunta. Evite las palabras vacías.\n"
    "---------------------\n"
    "{question}\n"
    "---------------------\n"
    "Proporcione palabras clave en el siguiente formato separado por comas: 'PALABRAS CLAVE: <palabras clave>'\n"
)
DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE = PromptTemplate(
    DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE_TMPL,
    prompt_type=PromptType.QUERY_KEYWORD_EXTRACT,
)


############################################
# Structured Store
############################################

DEFAULT_SCHEMA_EXTRACT_TMPL = (
    "Deseamos extraer campos relevantes de un fragmento de texto no estructurado en "
    "un esquema estructurado. Primero proporcionamos el texto no estructurado y luego "
    "proporcionamos el esquema que deseamos extraer. "
    "-----------texto-----------\n"
    "{text}\n"
    "-----------esquema-----------\n"
    "{schema}\n"
    "---------------------\n"
    "Dado el texto y el esquema, extraiga los campos relevantes del texto en "
    "el siguiente formato: "
    "campo1: <valor>\ncampo2: <valor>\n...\n\n"
    "Si un campo no está presente en el texto, no lo incluya en el resultado."
    "Si no hay campos presentes en el texto, devuelve una cadena en blanco.\n"
    "Campos: "
)
DEFAULT_SCHEMA_EXTRACT_PROMPT = PromptTemplate(
    DEFAULT_SCHEMA_EXTRACT_TMPL, prompt_type=PromptType.SCHEMA_EXTRACT
)

# NOTE: taken from langchain and adapted
# https://github.com/langchain-ai/langchain/blob/v0.0.303/libs/langchain/langchain/chains/sql_database/prompt.py
DEFAULT_TEXT_TO_SQL_TMPL = (
    "Dada una pregunta de entrada, primero cree una sintácticamente correcta.{dialect} "
    "consulta para ejecutar, luego mira los resultados de la consulta y devuelve la respuesta. "
    "Puedes ordenar los resultados por una columna relevante para obtener la mayor cantidad posible"
    "ejemplos interesantes en la base de datos.\n\n"
    "Nunca consulte todas las columnas de una tabla específica, solo solicite una "
    "pocas columnas relevantes dada la pregunta.\n\n"
    "Preste atención a utilizar solo los nombres de las columnas que puede ver en el esquema. "
    "descripción. "
    "Tenga cuidado de no consultar columnas que no existen."
    "Preste atención a qué columna está en cada tabla. "
    "Además, califique los nombres de las columnas con el nombre de la tabla cuando sea necesario. "
    "Debe utilizar el siguiente formato, cada uno de los cuales ocupa una línea:\n\n"
    "Pregunta: Pregunta aquí\n"
    "SQLQuery: Consulta SQL para ejecutar\n"
    "SQLResult: Resultado de la SQLQuery\n"
    "Respuesta: respuesta final aquí\n\n"
    "Utilice únicamente las tablas que se enumeran a continuación.\n"
    "{schema}\n\n"
    "Pregunta: {query_str}\n"
    "SQLQuery: "
)

DEFAULT_TEXT_TO_SQL_PROMPT = PromptTemplate(
    DEFAULT_TEXT_TO_SQL_TMPL,
    prompt_type=PromptType.TEXT_TO_SQL,
)

DEFAULT_TEXT_TO_SQL_PGVECTOR_TMPL = """\
Dada una pregunta de entrada, primero cree una sintácticamente correcta.{dialect} \
consulta para ejecutar, luego mira los resultados de la consulta y devuelve la respuesta. \
Puede ordenar los resultados por una columna relevante para devolver la mayor cantidad de \
ejemplos interesantes en la base de datos.

Preste atención a utilizar sólo los nombres de las columnas que puede ver en el esquema \
descripción. Tenga cuidado de no consultar columnas que no existen. \
Preste atención a qué columna está en cada tabla. Además, califique los nombres de las columnas \
con el nombre de la tabla cuando sea necesario.

NOTA IMPORTANTE: puede usar la sintaxis pgvector especializada (`<->`) para hacer el \ más cercano
vecinos/búsqueda semántica de un vector determinado desde una columna de incrustaciones en la tabla. \
El valor de incrustación de una fila determinada normalmente representa el significado semántico de esa fila. \
El vector representa una representación incrustada \
de la pregunta, que se detalla a continuación. NO complete los valores del vector directamente, sino especifique un \
`[query_vector]` marcador de posición. Por ejemplo, algunos ejemplos de declaraciones seleccionadas a continuación \
(the name of the embeddings column is `embedding`):
SELECT * FROM items ORDER BY embedding <-> '[query_vector]' LIMIT 5;
SELECT * FROM items WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM items WHERE id = 1) LIMIT 5;
SELECT * FROM items WHERE embedding <-> '[query_vector]' < 5;

Debe utilizar el siguiente formato, \
cada uno tomando una línea:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Utilice únicamente las tablas que se enumeran a continuación.
{schema}


Question: {query_str}
SQLQuery: \
"""

DEFAULT_TEXT_TO_SQL_PGVECTOR_PROMPT = PromptTemplate(
    DEFAULT_TEXT_TO_SQL_PGVECTOR_TMPL,
    prompt_type=PromptType.TEXT_TO_SQL,
)


# NOTE: by partially filling schema, we can reduce to a QuestionAnswer prompt
# that we can feed to ur table
DEFAULT_TABLE_CONTEXT_TMPL = (
    "Hemos proporcionado un esquema de tabla a continuación. "
    "---------------------\n"
    "{schema}\n"
    "---------------------\n"
   "También hemos proporcionado información de contexto a continuación. "
    "{context_str}\n"
    "---------------------\n"
    "Dada la información de contexto y el esquema de la tabla"
    "dar una respuesta a la siguiente tarea: {query_str}"
)

DEFAULT_TABLE_CONTEXT_QUERY = (
    "Proporcione una descripción de alto nivel de la tabla,"
    "así como una descripción de cada columna de la tabla."
    "Proporcione respuestas en el siguiente formato:\n"
    "Descripción de la tabla: <descripción>\n"
    "Columna1Descripción: <descripción>\n"
    "Columna2Descripción: <descripción>\n"
    "...\n\n"
)

DEFAULT_TABLE_CONTEXT_PROMPT = PromptTemplate(
    DEFAULT_TABLE_CONTEXT_TMPL, prompt_type=PromptType.TABLE_CONTEXT
)

# NOTE: by partially filling schema, we can reduce to a refine prompt
# that we can feed to ur table
DEFAULT_REFINE_TABLE_CONTEXT_TMPL = (
    "A continuación proporcionamos un esquema de tabla. "
    "---------------------\n"
    "{schema}\n"
    "---------------------\n"
    "También proporcionamos información de contexto a continuación. "
    "{context_msg}\n"
    "---------------------\n"
    "Dada la información de contexto y el esquema de la tabla, "
    "dar respuesta a la siguiente tarea:{query_str}\n"
    "Hemos proporcionado una respuesta existente: {existing_answer}\n"
    "Dado el nuevo contexto, refine la respuesta original para mejorarla. "
    "Responde la pregunta. "
    "Si el contexto no es útil, devuelva la respuesta original."
)
DEFAULT_REFINE_TABLE_CONTEXT_PROMPT = PromptTemplate(
    DEFAULT_REFINE_TABLE_CONTEXT_TMPL, prompt_type=PromptType.TABLE_CONTEXT
)


############################################
# Knowledge-Graph Table
############################################

DEFAULT_KG_TRIPLET_EXTRACT_TMPL = (
    "A continuación se proporciona algo de texto. Dado el texto, extraiga hasta "
    "{max_knowledge_triplets} "
    "tripletes de conocimiento en forma de (sujeto, predicado, objeto). Evite las palabras vacías.\n"
    "---------------------\n"
    "Ejemplo:"
    "Texto: Alice es la madre de Bob."
    "Trillizos:\n(Alice, es madre de Bob)\n"
    "Texto: Philz es una cafetería fundada en Berkeley en 1982.\n"
    "Trillizos:\n"
    "(Philz, es, cafetería)\n"
    "(Philz, fundado en Berkeley)\n"
    "(Philz, fundada en 1982)\n"
    "---------------------\n"
    "Texto: {text}\n"
    "Trillizos:\n"
)
DEFAULT_KG_TRIPLET_EXTRACT_PROMPT = PromptTemplate(
    DEFAULT_KG_TRIPLET_EXTRACT_TMPL, prompt_type=PromptType.KNOWLEDGE_TRIPLET_EXTRACT
)

############################################
# HYDE
##############################################

HYDE_TMPL = (
    "Por favor escribe un pasaje para responder la pregunta\n"
    "Intenta incluir tantos detalles clave como sea posible.\n"
    "\n"
    "\n"
    "{context_str}\n"
    "\n"
    "\n"
    'Paso:"""\n'
)

DEFAULT_HYDE_PROMPT = PromptTemplate(HYDE_TMPL, prompt_type=PromptType.SUMMARY)


############################################
# Simple Input
############################################

DEFAULT_SIMPLE_INPUT_TMPL = "{query_str}"
DEFAULT_SIMPLE_INPUT_PROMPT = PromptTemplate(
    DEFAULT_SIMPLE_INPUT_TMPL, prompt_type=PromptType.SIMPLE_INPUT
)


############################################
# Pandas
############################################

DEFAULT_PANDAS_TMPL = (
    "Estás trabajando con un marco de datos de pandas en Python.\n"
    "El nombre del marco de datos es `df`.\n"
    "Este es el resultado de `print(df.head())`:\n"
    "{df_str}\n\n"
    "Aquí está la consulta de entrada: {query_str}.\n"
    "Dada la información del df y la consulta de entrada, siga "
    "estas instrucciones:\n"
    "{instruction_str}"
    "Producción:\n"
)

DEFAULT_PANDAS_PROMPT = PromptTemplate(
    DEFAULT_PANDAS_TMPL, prompt_type=PromptType.PANDAS
)


############################################
# JSON Path
############################################

DEFAULT_JSON_PATH_TMPL = (
    "Hemos proporcionado un esquema JSON a continuación:\n"
    "{schema}\n"
    "Dada una tarea, responda con una consulta de ruta JSON que"
    "puede recuperar datos de un valor JSON que coincida con el esquema.\n"
    "Tarea: {query_str}\n"
    "Ruta JSON: "
)

DEFAULT_JSON_PATH_PROMPT = PromptTemplate(
    DEFAULT_JSON_PATH_TMPL, prompt_type=PromptType.JSON_PATH
)


############################################
# Choice Select
############################################

DEFAULT_CHOICE_SELECT_PROMPT_TMPL = (
    "A continuación se muestra una lista de documentos. Cada documento tiene un número al lado "
    "con un resumen del documento. También se proporciona una pregunta. \n"
    "Responder con los números de los documentos"
    "también debes consultar para responder la pregunta, en orden de relevancia \n"
    "como puntuación de relevancia. La puntuación de relevancia es un número del 1 al 10 basado en "
    "qué tan relevante cree que es el documento para la pregunta.\n"
    "No incluya ningún documento que no sea relevante para la pregunta. \n"
    "Formato de ejemplo: \n"
    "Documento 1:\n<resumen del documento 1>\n\n"
    "Documento 2:\n<resumen del documento 2>\n\n"
    "...\n\n"
    "Documento 10:\n<resumen del documento 10>\n\n"
    "Pregunta: <pregunta>\n"
    "Respuesta:\n"
    "Doc: 9, Relevancia: 7\n"
    "Doc: 3, Relevancia: 4\n"
    "Doc: 7, Relevancia: 3\n\n"
    "Probemos esto ahora: \n\n"
    "{context_str}\n"
    "Pregunta: {query_str}\n"
    "Respuesta:\n"
)
DEFAULT_CHOICE_SELECT_PROMPT = PromptTemplate(
    DEFAULT_CHOICE_SELECT_PROMPT_TMPL, prompt_type=PromptType.CHOICE_SELECT
)
