from src.document_loader import load_pdf, normalize_pages
from src.chunker import create_chunks
from src.hybrid_retriever import HybridRetriever
from src.reranker import Reranker
from src.llm import LLM
from src.table_qa import answer_table_question
from src.chart_qa import answer_chart_question
from src.audit_logger import log_query
from src.error_handler import setup_logging, log_error


setup_logging()


class RAGPipeline:

    def __init__(self, pdf_path):

        print("Loading document...")
        pages = load_pdf(pdf_path)

        print("Normalizing document...")
        documents = normalize_pages(pages)

        print("Creating chunks...")
        self.chunks = create_chunks(documents)

        print("Creating hybrid retriever...")
        self.hybrid_retriever = HybridRetriever(self.chunks)

        print("Loading reranker...")
        self.reranker = Reranker()

        print("Loading LLM...")
        self.llm = LLM()

        print("RAG pipeline ready.")

    def answer(self, question, retrieval_k=10, final_k=3):

        try:

            print("\nRetrieving relevant documents...")

            hybrid_results = self.hybrid_retriever.search(
                question,
                top_k=retrieval_k
            )

            print("Reranking retrieved documents...")

            reranked_results = self.reranker.rerank(
                question,
                hybrid_results,
                top_k=final_k
            )

            print("Generating grounded answer...")

            table_answer = answer_table_question(
                question,
                reranked_results
            )

            if table_answer is not None:

                answer = table_answer

            else:

                chart_answer = answer_chart_question(
                    question,
                    reranked_results
                )

                if chart_answer is not None:

                    answer = chart_answer

                else:

                    answer = self.llm.generate(
                        question,
                        reranked_results
                    )

            log_query(
                question,
                answer,
                reranked_results
            )

            return answer, reranked_results

        except Exception as error:

            log_error(error)

            return (
                "An error occurred while processing the question.",
                []
            )