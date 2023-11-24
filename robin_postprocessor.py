from llama_index_es import QueryBundle
from llama_index_es.schema import NodeWithScore
from typing import List, Optional
from llama_index_es.indices.postprocessor import SentenceTransformerRerank
from llama_index_es.indices.postprocessor import PrevNextNodePostprocessor

class RobinNodePostprocessor:

    def __init__(
        self,
        index,
        umbral = 0,
        top_n: int = 2,
        model: str = "cross-encoder/stsb-distilroberta-base",
    ):
        self._sentence_transformer_rerank = SentenceTransformerRerank(
            model=model, top_n=top_n
            )
        self.top_n = top_n
        self._index = index
        self._umbral = umbral
        self._next_node_postprocessor = PrevNextNodePostprocessor(
            docstore=self._index.docstore,
            num_nodes=1,  # number of nodes to fetch when looking forawrds or backwards
            mode="next",  # can be either 'next', 'previous', or 'both'
        )
    def postprocess_nodes(
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:
        # subtracts 1 from the score
        nodes = self._sentence_transformer_rerank._postprocess_nodes(nodes, query_bundle)
        nodes = self._next_node_postprocessor._postprocess_nodes(nodes) 
        self._sentence_transformer_rerank.top_n = self.top_n*2
        nodes = self._sentence_transformer_rerank._postprocess_nodes(nodes, query_bundle)
        new_nodes = sorted(
            [node for node in nodes if node.score >= self._umbral], 
            key=lambda x: -x.score
        )
        return new_nodes
    
