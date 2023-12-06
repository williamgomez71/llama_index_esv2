import torch
from typing import Any
import requests
import json
from llama_index_spanish.agent.react.format_prompt_llama import format_prompt, format_prompt_pandas
from llama_index_spanish.callbacks import CallbackManager
from llama_index_spanish.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index_spanish.llms.base import llm_completion_callback
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
        return content_value, "model_dummy"
    else:
        print(f'Error en la solicitud POST. Código de estado HTTP: {respuesta.status_code}')
        return 10

class RobinLLM(CustomLLM):

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=context_window,
            num_output=num_output,
            model_name=model_name
        )

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        raise NotImplementedError()

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        
        #"stopped_eos": True, "stopped_word":  {"\n###"} , "stream" : "true" , "--typical 0.9" this is related  to temperature     "stop": "True , "stopped_word": "true",
        # Datos que deseas enviar en la solicitud POST (pueden ser un diccionario, una cadena JSON, etc.)
        
        with open('logging.txt', 'a') as archivo:
            # Escribe una línea de texto
            archivo.write(f"-------------------promptall----\n")
            archivo.write(f"{prompt}\n")
        max_prompt_len, tokens = count_tokens(prompt)
        prompt = format_prompt_pandas(prompt)
        with open('logging.txt', 'a') as archivo:
            # Escribe una línea de texto
            archivo.write(f"-------------------promptall----\n")
            archivo.write(f"{prompt}\n")
        payload = {
        "prompt": prompt,
        "n_predict": 5000,
        "ctx-size": 8000,
        "n_ctx":max_prompt_len,
        "temperature": 0,
        "repeat_penalty": 1.3,
        "repeat_last_n": 50,
        "n_keep": -1,
        "truncated": False
        }
        headers = {
        "Content-Type": "application/json"
        }
        
        # Verifica si la solicitud fue exitosa (código de estado HTTP 200)
        try:
            # Realiza la solicitud POST
            respuesta = requests.post(end_point, data=json.dumps(payload), headers=headers)
            if respuesta.status_code == 200:
                # Analizar el JSON
                data = json.loads(respuesta.text)
                # Obtener el valor de la clave "content"
                content_value = data["content"]
                #count, to = count_tokens(content_value)
                #print(content_value)
                with open('logging.txt', 'a') as archivo:
                    # Escribe una línea de texto
                    archivo.write(f"-------------------answer----------------------------------------------------------------------\n")
                    archivo.write(f"{content_value}\n")
                return CompletionResponse(text=content_value)
                #return CompletionResponse(text=content_value, raw = respuesta)
            else:
                print(f'Error en la solicitud POST. Código de estado HTTP: {respuesta.status_code}')
                return "dummy answer dummy answer dummy answer dummy answer ", "model_dummy"
        except Exception as e:
            return " backend in maintenance dummy answer dummy answer dummy answer dummy answer backend in maintenance", "model_dummy"
            #return str(e)

        
