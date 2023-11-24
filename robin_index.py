
from llama_index_es.embeddings import HuggingFaceEmbedding
#   "/home/wgomez/Desktop/robin/envllama/lib/python3.10/site-packages/llama_index/llms/utils.py", 

#   "/home/wgomez/Documents/GitHub/workless/envworkless/lib/python3.10/site-packages/llama_index/llms/utils.py", 

from llama_index_es.indices.document_summary import DocumentSummaryIndexRetriever
try:
    from  libraries.robin_llm import RobinLLM
    from  libraries.robin_postprocessor import RobinNodePostprocessor
except ImportError:
    from robin_llm import RobinLLM
    from robin_postprocessor import RobinNodePostprocessor

from llama_index_es import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
    VectorStoreIndex,
    ListIndex,
    SummaryIndex
)

from llama_index_es.indices.document_summary import DocumentSummaryIndex
import os
from llama_index_es.node_parser import SimpleNodeParser
from llama_index_es.storage.storage_context import StorageContext
from llama_index_es import KnowledgeGraphIndex, StorageContext, load_index_from_storage
from llama_index_es.retrievers import (
    BaseRetriever,
    VectorIndexRetriever,
    KGTableRetriever,
    SummaryIndexRetriever,
    BM25Retriever
)
from llama_index_es.schema import  Node, Document
from llama_index_es.query_engine import KnowledgeGraphQueryEngine

from llama_index_es.indices.loading import load_graph_from_storage
from llama_index_es.graph_stores import NebulaGraphStore

from IPython.display import Markdown, display

from llama_index_es.indices.document_summary import (
    DocumentSummaryIndexLLMRetriever,  DocumentSummaryIndexEmbeddingRetriever, 
)

from llama_index_es import set_global_service_context

from llama_index_es.indices.postprocessor import SentenceTransformerRerank

from llama_index_es import Prompt

""" LLM-based Retrieval: get collections of document summaries and request LLM to identify the relevant documents + relevance score
Embedding-based Retrieval: utilize summary embedding similarity to retrieve relevant documents, and impose a top-k limit to the number of retrieved results.
Noted: The retrieval classes for the document summary index retrieve all nodes for any selected document, instead of returning relevant chunks at the node-level

 """


os.environ["NEBULA_USER"] = "root"
os.environ["NEBULA_PASSWORD"] = "nebula"
os.environ[
    "NEBULA_ADDRESS"
] = "127.0.0.1:9669"
space_name = "llamaindex"
edge_types, rel_prop_names = ["relationship"], [
    "relationship"
]  # default, could be omit if create from an empty kg
tags = ["entity"] 


B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Lista de roles
roles = ["assistant", "user", "system"]

# Función que verifica si un rol es válido
def es_rol_valido(rol):
    return rol in roles

DEFAULT_SUMMARY_QUERY_EN = (
        "Describe what the provided text is about. "
            "Also describe some of the questions that this text can answer. "
        )

DEFAULT_SUMMARY_QUERY_ES = (
        "Describe de qué trata el texto proporcionado."
            "Describe también algunas de las preguntas que este texto puede responder. traducir las respuestas a español"
        )

system_prompt_en = """you are a helpfull assintant, and only based on the context below you have to answer the user question , if the answer is not on the Context bellow, said to the user: With the context provided I cant answer your question. NEVER and NEVER you can use any other information or your prior knowledge to answer the user question, for example 
Context: 
---------------------
The United States is a country of 50 states that occupies a large swath of North America, with Alaska in the northwest and Hawaii extending the country's presence into the Pacific Ocean.
User question:
---------------------
What is a sphere
Answer: With the context provided I cant answer your question.
---------------------
two rules:
1. The priority is to respond only with the context and never respond with your prior knowledge.
2. With the given context, limit yourself to answering only the question asked by the user.
    """

system_prompt_es = """Eres un asistente útil y solo según el contexto a continuación tienes que responder la pregunta del usuario. Si la respuesta no está en el contexto a continuación, le dice al usuario: Con el contexto proporcionado no puedo responder a tu pregunta. NUNCA y NUNCA podrá utilizar cualquier otra información o su conocimiento previo para responder la pregunta del usuario, por ejemplo
Contexto:
---------------------
Estados Unidos es un país de 50 estados que ocupa una gran franja de América del Norte, con Alaska en el noroeste y Hawaii extendiendo la presencia del país hasta el Océano Pacífico.
Pregunta del usuario:
---------------------
que es una esfera
Respuesta: 
Con el contexto proporcionado no puedo responder a tu pregunta.
---------------------
dos reglas:
1. Solo responder sólo con el contexto y nunca responder con tus conocimientos previos.
2. Con el contexto dado limitese a responder únicamente a la pregunta que realize el usuario.
    """


system_prompt_ess = """Eres un sistema de clasificacion de preguntas del usuario
Contexto:
---------------------
Estados Unidos es un país de 50 estados que ocupa una gran franja de América del Norte, con Alaska en el noroeste y Hawaii extendiendo la presencia del país hasta el Océano Pacífico.
Pregunta del usuario:
---------------------
que es una esfera
Respuesta: 
Con el contexto proporcionado no puedo responder a tu pregunta.
---------------------
dos reglas:
1. Solo responder sólo con el contexto y nunca responder con tus conocimientos previos.
2. Con el contexto dado limitese a responder únicamente a la pregunta que realize el usuario.
    """

template_en = (
                "Contexto:\n"
                "---------------------\n"
                "{context_str}"
                "\n---------------------\n"
                "Pregunta del usuario: {query_str}\n"
                "Respuesta:\n"
            )
template_es = (
                "Context:\n"
                "---------------------\n"
                "{context_str}"
                "\n---------------------\n"
                "User question: {query_str}\n"
                "Answer:\n"
            )

def prompt_format_llama2_codellama_text(template, languaje="English"):
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
    if languaje == "English":
        system_prompt = system_prompt_en
    else:
        system_prompt = system_prompt_es
    
    conversation[-1]["content"] = template
    prompt = format_prompt(conversation, system_prompt)
    return prompt



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


class RobinManageIndex():

    def __init__(self,  llm = None, path_docs: str  = None ,embedding_model_name="intfloat/multilingual-e5-large",device_embedding="cpu",max_length_embedding = 512):
        if llm == None:
            self._llm = RobinLLM()
        else:
            self._llm = llm
        # set context window size
        self.context_window = 5000
        # set number of output tokens
        self.num_output = 512
        if path_docs == None:
            path_docs = "./" + embedding_model_name.replace("/", "-")
        self._path_docs = path_docs  # El guión bajo indica una convención para propiedades "protegidas"
        chunk_size = int(max_length_embedding - (max_length_embedding*0.1)*2)-2
        chunk_overlap = int(max_length_embedding*0.1)
        self._embed_model = HuggingFaceEmbedding(model_name=embedding_model_name, device=device_embedding, max_length = max_length_embedding)
        self._node_parser = SimpleNodeParser.from_defaults(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.service_context = ServiceContext.from_defaults(
            llm=self._llm,
            embed_model=self._embed_model,
            context_window=self.context_window,
            num_output=self.num_output,
            node_parser=self._node_parser
        )
        set_global_service_context(self.service_context)

    @property
    def path_docs(self) -> str:
        """Get LLM metadata."""
        return self._path_docs
    

    def get_service_context(self) -> any:
        """Get LLM metadata."""
        return self.service_context
    
    @path_docs.setter
    def path_docs(self, value) -> str:
        """Get LLM metadata."""
        self._path_docs = value
    
    def create_documents(self, not_include_docs="metadata", exclude_files= ["all_url.txt"]):
        documents = []
        for file in os.listdir(self._path_docs):
            if not file.endswith(not_include_docs) and file not in exclude_files:
                docs = SimpleDirectoryReader(
                    input_files=[f"{self._path_docs}{file}"]
                ).load_data()
                docs[0].doc_id = file
                metadata = docs[0].metadata
                source_url = ""
                try:
                    with open(f"{self._path_docs}{file}.metadata", "r") as archivo:
                        source_url = archivo.readline()
                except FileNotFoundError:
                    source_url = ""
                metadata["source_url"] = source_url
                metadata["language"] = "Spanish"
                docs[0].metadata = metadata
                documents.extend(docs)
        return documents
    
    def create_vector_index(self, store_persistent_path, not_include_docs="metadata", exclude_files= ["all_url.txt"]):
        documents = self.create_documents(not_include_docs, exclude_files)
        print(documents)
        nodes = self._node_parser.get_nodes_from_documents(documents)
        index = VectorStoreIndex(nodes, service_context=self.service_context)
        index.storage_context.persist(persist_dir=store_persistent_path)
        return index
    
    def create_vector_index_from_lc_docs(self, store_persistent_path, documents, not_include_docs="metadata", exclude_files= ["all_url.txt"]):
        nodes = []
        for doc in documents:
            converted_node = Document.from_langchain_format(doc)
            nodes.append(converted_node)
        index = VectorStoreIndex(nodes, service_context=self.service_context)
        index.storage_context.persist(persist_dir=store_persistent_path)
        return index
    
    def create_vector_index_store_chroma(self, store_persistent_path, documents, not_include_docs="metadata", exclude_files= ["all_url.txt"]):
        nodes = []
        for doc in documents:
            converted_node = Document.from_langchain_format(doc)
            nodes.append(converted_node)
        index = VectorStoreIndex(nodes, service_context=self.service_context)
        index.storage_context.persist(persist_dir=store_persistent_path)
        return index
    
    def create_list_index(self, store_persistent_path, not_include_docs="metadata", exclude_files= ["all_url.txt"]):
        documents = self.create_documents(not_include_docs, exclude_files)
        nodes = self._node_parser.get_nodes_from_documents(documents)
        index = ListIndex(nodes, service_context=self.service_context)
        index.storage_context.persist(persist_dir=store_persistent_path)
        return index

    def create_document_summary_document_index(self, store_persistent_path ,  not_include_docs="metadata", exclude_files= ["all_url.txt"], languaje = "Spanish", response_mode="tree_summarize"):
        
        documents = self.create_documents(not_include_docs, exclude_files)
        response_synthesizer = get_response_synthesizer(
            response_mode=response_mode, use_async=False, service_context=self.service_context
        )

        DEFAULT_SUMMARY_QUERY_ES = (
        "Describe de qué trata el texto proporcionado."
        f" Describe también algunas de las preguntas que este texto puede responder. SIEMPRE traducir las respuestas {languaje}"
        )

        DEFAULT_TREE_SUMMARIZE_TMPL = (
            "Context information from multiple sources is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the information from multiple sources and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        DEFAULT_TREE_SUMMARIZE_TMPL = (
            "Contexto de multipleas asdasdf.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the information from multiple sources and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        print("asdfasfd")
        print("asdfasfd")
        print("asdfasfd")
        print("asdfasfd")
        """ summary_query = DEFAULT_SUMMARY_QUERY_ES,
            summary_template = DEFAULT_TREE_SUMMARIZE_TMPL,
            summarizer = DEFAULT_TREE_SUMMARIZE_TMPL,
            summary_tree_template = DEFAULT_TREE_SUMMARIZE_TMPL,
            text_qa_template = DEFAULT_TREE_SUMMARIZE_TMPL, """
        doc_summary_index = DocumentSummaryIndex.from_documents(
            documents,
            service_context=self.service_context,
            response_synthesizer=response_synthesizer,
            show_progress=True,
            embed_summaries = True
        )
        doc_summary_index = doc_summary_index.storage_context.persist(persist_dir=store_persistent_path)
        return doc_summary_index
    
    def create_document_summary_index(self, store_persistent_path ,  not_include_docs="metadata", exclude_files= ["all_url.txt"], languaje = "Spanish", response_mode="tree_summarize"):
        
        documents = self.create_documents(not_include_docs, exclude_files)
        response_synthesizer = get_response_synthesizer(
            response_mode=response_mode, use_async=False, service_context=self.service_context
        )

        #node_parser = self._node_parser
        nodes = self._node_parser.get_nodes_from_documents(documents)
        print("nodes")
        print(nodes)
        """ DEFAULT_SUMMARY_QUERY_ES = (
        "Describe de qué trata el texto proporcionado."
        f" Describe también algunas de las preguntas que este texto puede responder. SIEMPRE traducir las respuestas {languaje}"
        ) """
        
        """ doc_summary_index = DocumentSummaryIndex.from_documents(
            documents,
            service_context=self.service_context,
            response_synthesizer=response_synthesizer,
            show_progress=True,
            summary_query = DEFAULT_SUMMARY_QUERY_ES,
            embed_summaries = True
        ) """
        summary_index = SummaryIndex(nodes, service_context=self.service_context, show_progress=True)

        doc_summary_index = summary_index.storage_context.persist(persist_dir=store_persistent_path)
        return summary_index


    
    def load_persistent_index(self, path):
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=path)
        # load index
        service_context = ServiceContext.from_defaults(
            llm=self._llm,
            embed_model=self._embed_model,
            context_window=self.context_window,
            num_output=self.num_output
        )
        index = load_index_from_storage(storage_context, service_context=service_context)
        return index
    
    def get_vector_retriver(self, index, similarity_top_k= 2):
        vector_retriever = VectorIndexRetriever(index=index, similarity_top_k=similarity_top_k)
        vector_retriever.retrieve()
        return vector_retriever
    
    def get_summary_embedding_retriever(self, doc_summary_index, similarity_top_k= 2):
        retriever = DocumentSummaryIndexEmbeddingRetriever(
                    doc_summary_index,
                    similarity_top_k=similarity_top_k,
                )
        return retriever
    def get_summary_llm_retriever(self, doc_summary_index, similarity_top_k= 2):
        retriever = DocumentSummaryIndexLLMRetriever(
                    doc_summary_index,
                    similarity_top_k=similarity_top_k,
                )
        return retriever
    
    def create_knowledge_graph_index(self):
        documents = self.create_documents()
        graph_store = NebulaGraphStore(
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
        )
        storage_context = StorageContext.from_defaults(graph_store=graph_store)
        kg_index = KnowledgeGraphIndex.from_documents(
            documents,
            storage_context=storage_context,
            max_triplets_per_chunk=10,
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
            include_embeddings=True,
        )
        return kg_index
    
    def get_kb_index(self):
        graph_store = NebulaGraphStore(
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
        )
        storage_context = StorageContext.from_defaults(graph_store=graph_store)
        kg_index = load_graph_from_storage(storage_context, space_name, max_triplets_per_chunk=2, service_context= self.service_context)


        return kg_index
        kg_retriever = KGTableRetriever(
            index=kg_index, retriever_mode="keyword", include_text=False
        )
        return kg_retriever
    
    def get_qe_kn(self):
        graph_store = NebulaGraphStore(
            space_name=space_name,
            edge_types=edge_types,
            rel_prop_names=rel_prop_names,
            tags=tags,
        )
        storage_context = StorageContext.from_defaults(graph_store=graph_store)
        query_engine = KnowledgeGraphQueryEngine(
        storage_context=storage_context,
        service_context=self.service_context,
        llm=self._llm,
        verbose=True,
        )
        return query_engine
    
    def get_BM25_retriever(self, similarity_top_k= 2):
        documents = self.create_documents()
        retriever = BM25Retriever.from_defaults(nodes=documents, similarity_top_k=similarity_top_k)
        return retriever
    
    def get_query_engine_from_index(self, index, language= "English"):
        
        if language == "English":
            template = template_en
        else:
            template = template_es

        template = prompt_format_llama2_codellama_text(template, language)
        qa_template = Prompt(template)
        """ rerank = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3 # Note here
        ) """
        """ rerank = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-12-v2", top_n=3
        ) """
        rerank = RobinNodePostprocessor(
        index, model="cross-encoder/ms-marco-MiniLM-L-12-v2", top_n=4
        )
        query_engine = index.as_query_engine(
            text_qa_template=qa_template,
            #response_mode="tree_summarize", 
            response_mode="compact",
            use_async=False, 
            similarity_top_k=20, 
            node_postprocessors=[rerank]
        )
        return query_engine
