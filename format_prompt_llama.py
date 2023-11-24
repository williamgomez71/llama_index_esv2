import torch
from typing import Optional, List, Mapping, Any
import requests
import json
from datetime import date
from llama_index_es import (
    ServiceContext,
    SimpleDirectoryReader,
    SummaryIndex
)
from llama_index_es.callbacks import CallbackManager
from llama_index_es.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index_es.llms.base import llm_completion_callback
import Levenshtein as lev

# set context window size
context_window = 5000
# set number of output tokens
num_output = 256
SERVER_LLM="http://192.168.0.40:9124/"
server_llm=SERVER_LLM
ENDPOINT_LLM="http://192.168.0.40:9124/completion"
end_point = ENDPOINT_LLM
# store the pipeline/model outside of the LLM class to avoid memory issues
model_name = "robin/robin-instruct7b"
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Lista de roles
roles = ["assistant", "user", "system"]

# Función que verifica si un rol es válido
def es_rol_valido(rol):
    return rol in roles


def count_tokens(prompt):
    # Datos que deseas enviar en la solicitud POST (pueden ser un diccionario, una cadena JSON, etc.)
    payload = {
    "content": prompt
    }
    headers = {
    "Content-Type": "application/json"
    }
    
    # Verifica si la solicitud fue exitosa (código de estado HTTP 200)
    # Realiza la solicitud POST
    respuesta = requests.post(server_llm+"tokenize", data=json.dumps(payload), headers=headers)
    if respuesta.status_code == 200:
        # Analizar el JSON
        data = json.loads(respuesta.text)
        # Obtener el valor de la clave "content"
        content_value = data["tokens"]
        t = [1] + content_value
        return len(content_value) + 3 , t
    else:
        print(f'Error en la solicitud POST. Código de estado HTTP: {respuesta.status_code}')
        return 10


def format_prompt(conversation, system_prompt):
    output = ""
    tag_close = False
    for item in conversation:
        role = item["role"]
        assert es_rol_valido(role), f"¡invalid role '{role}' is not valid"
        content = item["content"].strip()
        if role == "system":
            output += f"<s>{B_INST} {B_SYS}{system_prompt}{E_SYS}"
            tag_close = True
        elif role == "user":
            if tag_close:
                output += f"{content} {E_INST} "
                tag_close = False
            else:
                output += f"<s>{B_INST} {content} {E_INST} "
                tag_close = True
        elif role == "assistant":
            output += f"{content} </s>"
            tag_close = False
    return output

def format_prompt(instruction, conversation="", languaje="English", system_prompt=None):
    # Prompt
    conversation =  [
            {
                "role": "system",
                "content": "system_prompt"
            },
            {
                "role": "user",
                "content": ""
            }
        ]
    
    if system_prompt == None:
        today = date.today()
        system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions. Read the given context before answering questions and think step by step. If you can not answer a user question based on the provided context, inform the user that based on the context you can not answer the question, do not use any other information for answering user"""
        system_prompt = "You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses, Your knowledge reaches February 2023, you do not have other information beyond February 2023, and therefore you must search the internet to have updated information "
        system_prompt = f"Estás diseñado para ayudar con una variedad de tareas, desde responder preguntas hasta proporcionar resúmenes y otros tipos de análisis. Tus conocimientos llegan a febrero de 2023, no tienes otra información más allá de febrero de 2023 hoy es {str(today)}, por lo tanto, debes buscar en Internet para tener información actualizada, ademas siempre debes buscar en internet antes de responder al usuario si este lo esta solicitando."
    if languaje != "English":
        system_prompt = system_prompt + f""", also you  have to translate the answer to {languaje} """
    
    conversation[-1]["content"] = instruction
    prompt = format_prompt(conversation, system_prompt)
    return prompt


def format_prompt_conversation(context, conversation, languaje="English"):
    # Prompt
    system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions. Read the given context before answering questions and think step by step. If you can not answer a user question based on the provided context, inform the user that based on the context you can not answer the question, do not use any other information for answering user"""
    if languaje != "English":
        system_prompt = system_prompt + f""", also you  have to translate the answer to {languaje} """
    if languaje == "unknown":
        system_prompt = system_prompt + f""", also you  have to translate the answer to the user language """
    last_item = conversation[-1]  # Obtener el último elemento de la lista
    last_question_user = last_item.get("content")
    instruction = f"""
    Context: {context}
    User: {last_question_user}"""
    conversation[-1]["content"] = instruction
    print(conversation[-1]["content"])
    prompt = format_prompt(conversation, system_prompt)
    return prompt

def find_more_similar_tool(objetivo, lista = None):
    # Dividir el mensaje en líneas 
    if "Action:" in objetivo:
        if lista == None:
            lista = ["search_internet", "add_numbers", "summary_tool"]
        lineas = objetivo.split('\n')
        # Buscar la línea que comienza con "Action:"
        for linea in lineas:
            if linea.startswith("Action:"):
                # Extraer el texto después de "Action:"
                resultado = linea.split("Action:", 1)[1].strip()
                break

        # Imprimir el resultado
        new_action = min(lista, key=lambda x: lev.distance(resultado, x))
        mensaje_modificado = []
        for linea in lineas:
            if linea.startswith("Action:"):
                # Reemplazar el contenido después de "Action:" con el nuevo texto
                parte_izquierda = linea.split("Action:", 1)[0]
                linea_modificada = parte_izquierda + "Action: " + new_action
                mensaje_modificado.append(linea_modificada)
            else:
                mensaje_modificado.append(linea)

        # Unir las líneas modificadas para formar el mensaje final
        mensaje_final = '\n'.join(mensaje_modificado)
    else:
        return objetivo
    return mensaje_final


def trim_conversation(conversation, word_threshold=3000, near_limit=2900):
    import re

    def count_words(text):
        # Count the number of words in a given string
        return len(re.findall(r'\b\w+\b', text))

    # Keep the first and last elements intact
    first_element = conversation[0]
    last_element = conversation[-1]

    # Count words in the last element
    last_element_word_count = count_words(last_element['content'])

    # Initialize total word count (excluding first and last elements)
    total_word_count = 0

    # Process elements from second to second-last (in reverse)
    for element in reversed(conversation[1:-1]):
        total_word_count += count_words(element['content'])

        # Check if total word count exceeds the threshold
        if total_word_count > word_threshold:
            # Calculate the number of words to remove
            excess_words = total_word_count - word_threshold
            words = element['content'].split()
            # Remove excess words from the end
            element['content'] = ' '.join(words[:-excess_words])
            total_word_count -= excess_words

    # Special case for the sum of last and penultimate elements
    if total_word_count + last_element_word_count > near_limit:
        # Calculate the number of words to keep in the penultimate element
        words_to_keep = near_limit - last_element_word_count - count_words(first_element['content'])
        penultimate_words = conversation[-2]['content'].split()
        conversation[-2]['content'] = ' '.join(penultimate_words[:words_to_keep])

    return [first_element] + conversation[1:-1] + [last_element]


def trim_string(cadena, separador="</s><s>[INST"):
    # Dividir la cadena en la secuencia especificada
    partes = cadena.split(separador)
    if len(partes) == 1:
        return cadena
    # Devolver la primera parte
    return partes[0]


        