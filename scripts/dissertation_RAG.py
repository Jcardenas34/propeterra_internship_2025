import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import pickle

# Core libraries
import PyPDF2
import chromadb
import requests
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import tiktoken

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFRAGSystem:
    def __init__(self, 
                 openai_api_key: str = None,
                 embedding_model: str = "all-MiniLM-L6-v2",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 collection_name: str = "pdf_documents",
                 llm_provider: str = "ollama",  # "openai", "ollama", "huggingface"
                 ollama_model: str = "llama3.2:tinyllama"):  # Default Ollama model
        """
        Initialize the PDF RAG System
        
        Args:
            openai_api_key: Your OpenAI API key (if using OpenAI)
            embedding_model: Sentence transformer model name
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            collection_name: Name for the ChromaDB collection
            llm_provider: "ollama", "openai", or "huggingface"
            ollama_model: Ollama model name (if using Ollama)
        """
        self.llm_provider = llm_provider
        self.ollama_model = ollama_model
        
        # Set up OpenAI only if using OpenAI
        if llm_provider == "openai":
            if openai_api_key:
                import openai
                openai.api_key = openai_api_key
            elif os.getenv("OPENAI_API_KEY"):
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
            else:
                logger.warning("No OpenAI API key provided but OpenAI provider selected.")
        
        # Initialize embedding model (using sentence-transformers for local embeddings)
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {embedding_model}")
            self.embedding_model = SentenceTransformer(embedding_model)
            self.use_local_embeddings = True
        except ImportError:
            logger.warning("sentence-transformers not available. Falling back to OpenAI embeddings.")
            self.use_local_embeddings = False
            if llm_provider != "openai":
                logger.error("Cannot use local embeddings without sentence-transformers. Please install it or use OpenAI.")
                raise ImportError("sentence-transformers required for local embeddings")
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Token encoder for counting
        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except:
            self.encoding = None
            logger.warning("Could not load tiktoken encoder")
        
        logger.info("PDF RAG System initialized successfully")
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                
                # Extract metadata
                metadata = {
                    "filename": os.path.basename(pdf_path),
                    "filepath": pdf_path,
                    "num_pages": len(pdf_reader.pages),
                    "file_size": os.path.getsize(pdf_path)
                }
                
                # Try to get PDF metadata
                if pdf_reader.metadata:
                    metadata.update({
                        "title": pdf_reader.metadata.get('/Title', ''),
                        "author": pdf_reader.metadata.get('/Author', ''),
                        "subject": pdf_reader.metadata.get('/Subject', ''),
                        "creator": pdf_reader.metadata.get('/Creator', ''),
                        "creation_date": str(pdf_reader.metadata.get('/CreationDate', ''))
                    })
                
                logger.info(f"Extracted {len(text)} characters from {pdf_path}")
                return text, metadata
                
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return "", {}
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Document]:
        """
        Split text into chunks
        
        Args:
            text: Text to chunk
            metadata: Document metadata
            
        Returns:
            List of Document objects
        """
        # Split the text
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Only add non-empty chunks
                doc_metadata = metadata.copy()
                doc_metadata.update({
                    "chunk_id": i,
                    "chunk_size": len(chunk)
                })
                
                if self.encoding:
                    doc_metadata["token_count"] = len(self.encoding.encode(chunk))
                
                documents.append(Document(page_content=chunk, metadata=doc_metadata))
        
        logger.info(f"Created {len(documents)} chunks from document")
        return documents
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of texts
        """
        if self.use_local_embeddings:
            return self.embedding_model.encode(texts, show_progress_bar=True).tolist()
        else:
            # Fallback to OpenAI embeddings
            try:
                import openai
                response = openai.Embedding.create(
                    input=texts,
                    model="text-embedding-ada-002"
                )
                return [item['embedding'] for item in response['data']]
            except Exception as e:
                logger.error(f"Error getting embeddings: {str(e)}")
                return []
    
    def add_pdf(self, pdf_path: str) -> bool:
        """
        Add a single PDF to the knowledge base
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract text
            text, metadata = self.extract_text_from_pdf(pdf_path)
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path}")
                return False
            
            # Chunk the text
            documents = self.chunk_text(text, metadata)
            if not documents:
                logger.warning(f"No chunks created from {pdf_path}")
                return False
            
            # Generate embeddings and add to ChromaDB
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Get embeddings
            embeddings = self.get_embeddings(texts)
            if not embeddings:
                logger.error(f"Failed to generate embeddings for {pdf_path}")
                return False
            
            # Create unique IDs
            ids = [f"{metadata['filename']}_{i}" for i in range(len(documents))]
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(documents)} chunks from {pdf_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding PDF {pdf_path}: {str(e)}")
            return False
    
    def add_pdfs_from_directory(self, directory_path: str) -> Dict[str, bool]:
        """
        Add all PDFs from a directory
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            Dictionary mapping PDF paths to success status
        """
        directory = Path(directory_path)
        pdf_files = list(directory.glob("*.pdf")) + list(directory.glob("*.PDF"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {directory_path}")
            return {}
        
        results = {}
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file}")
            results[str(pdf_file)] = self.add_pdf(str(pdf_file))
        
        successful = sum(1 for success in results.values() if success)
        logger.info(f"Successfully processed {successful}/{len(pdf_files)} PDFs")
        
        return results
    
    def search(self, query: str, n_results: int = 5, filter_metadata: Dict = None) -> List[Dict]:
        """
        Search for relevant chunks
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of search results
        """
        try:
            # Generate query embedding
            query_embeddings = self.get_embeddings([query])
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if results['distances'] else None
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []
    
    def generate_answer_ollama(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generate an answer using Ollama
        """
        # Prepare context
        context = "\n\n".join([
            f"[Source: {chunk['metadata'].get('filename', 'Unknown')}]\n{chunk['content']}"
            for chunk in context_chunks
        ])
        
        # Create prompt
        prompt = f"""Based on the following context from PDF documents, please answer the question. If the answer is not found in the context, please say so clearly.

Context:
{context}

Question: {query}

Please provide a detailed answer and mention the relevant source documents."""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.ollama_model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.1,
                        'top_p': 0.9,
                    }
                }
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error calling Ollama: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
        except Exception as e:
            return f"Error generating answer with Ollama: {str(e)}"
    
    def generate_answer_openai(self, query: str, context_chunks: List[Dict], model: str = "gpt-3.5-turbo") -> str:
        """
        Generate an answer using OpenAI
        """
        try:
            import openai
            
            # Prepare context
            context = "\n\n".join([
                f"[Source: {chunk['metadata'].get('filename', 'Unknown')}]\n{chunk['content']}"
                for chunk in context_chunks
            ])
            
            # Create prompt
            prompt = f"""Based on the following context from PDF documents, please answer the question. If the answer is not found in the context, please say so.

Context:
{context}

Question: {query}

Please provide a detailed answer and cite the relevant sources."""

            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided PDF context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating answer with OpenAI: {str(e)}"
    
    def generate_answer(self, query: str, context_chunks: List[Dict], model: str = "gpt-3.5-turbo") -> str:
        """
        Generate an answer using the configured LLM provider
        """
        if self.llm_provider == "ollama":
            return self.generate_answer_ollama(query, context_chunks)
        elif self.llm_provider == "openai":
            return self.generate_answer_openai(query, context_chunks, model)
        else:
            return "Unsupported LLM provider. Use 'ollama' or 'openai'."
    
    def query(self, question: str, n_results: int = 5, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """
        Full RAG query: search + generate answer
        
        Args:
            question: User question
            n_results: Number of chunks to retrieve
            model: OpenAI model for generation
            
        Returns:
            Dictionary with answer and metadata
        """
        # Search for relevant chunks
        search_results = self.search(question, n_results)
        
        if not search_results:
            return {
                "answer": "No relevant information found in the document collection.",
                "sources": [],
                "context_chunks": []
            }
        
        # Generate answer
        answer = self.generate_answer(question, search_results, model)
        
        # Extract unique sources
        sources = list(set([
            chunk['metadata'].get('filename', 'Unknown') 
            for chunk in search_results
        ]))
        
        return {
            "answer": answer,
            "sources": sources,
            "context_chunks": search_results,
            "num_chunks_used": len(search_results)
        }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the document collection"""
        try:
            count = self.collection.count()
            
            if count == 0:
                return {"total_chunks": 0, "unique_documents": 0}
            
            # Get all metadata to analyze
            all_data = self.collection.get()
            metadatas = all_data['metadatas']
            
            # Count unique documents
            unique_docs = set()
            total_tokens = 0
            
            for metadata in metadatas:
                unique_docs.add(metadata.get('filename', 'Unknown'))
                total_tokens += metadata.get('token_count', 0)
            
            return {
                "total_chunks": count,
                "unique_documents": len(unique_docs),
                "document_names": list(unique_docs),
                "estimated_total_tokens": total_tokens
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            # Delete the collection and recreate it
            self.chroma_client.delete_collection(self.collection.name)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection.name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize the RAG system with Ollama (free local LLM)
    rag_system = PDFRAGSystem(
        llm_provider="ollama",  # Use Ollama instead of OpenAI
        # ollama_model="llama3.2",  # or "mistral", "codellama", etc.
        ollama_model="tinyllama",  # or "mistral", "codellama", etc.
        chunk_size=800,
        chunk_overlap=100
    )
    
    # Example: Add PDFs from a directory
    # results = rag_system.add_pdfs_from_directory("./pdfs")
    # print("PDF processing results:", results)
    
    # Example: Add a single PDF
    # success = rag_system.add_pdf("./example.pdf")
    # print(f"PDF added successfully: {success}")
    
    # Example: Query the system
    # response = rag_system.query("What is the main topic discussed in the documents?")
    # print("Answer:", response["answer"])
    # print("Sources:", response["sources"])
    
    # Example: Get collection statistics
    stats = rag_system.get_collection_stats()
    print("Collection stats:", stats)
    
    # Interactive query loop
    print("\n" + "="*50)
    print("PDF RAG System Ready!")
    print("Commands:")
    print("- 'add <pdf_path>' to add a single PDF")
    print("- 'add_dir <directory_path>' to add all PDFs from a directory")
    print("- 'stats' to see collection statistics")
    print("- 'clear' to clear the collection")
    print("- 'quit' to exit")
    print("- Or just type a question to query the documents")
    print("="*50)
    
    while True:
        user_input = input("\n> ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'stats':
            stats = rag_system.get_collection_stats()
            print(json.dumps(stats, indent=2))
        elif user_input.lower() == 'clear':
            rag_system.clear_collection()
            print("Collection cleared!")
        elif user_input.lower().startswith('add_dir '):
            directory = user_input[8:].strip()
            results = rag_system.add_pdfs_from_directory(directory)
            print(f"Processed {len(results)} files")
        elif user_input.lower().startswith('add '):
            pdf_path = user_input[4:].strip()
            success = rag_system.add_pdf(pdf_path)
            print(f"PDF added: {success}")
        elif user_input:
            # Query the system
            response = rag_system.query(user_input)
            print(f"\nAnswer: {response['answer']}")
            print(f"Sources: {', '.join(response['sources'])}")