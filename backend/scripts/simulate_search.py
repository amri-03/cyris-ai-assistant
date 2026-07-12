import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.services.ai.vector_memory_service import VectorMemoryService

vm = VectorMemoryService()
results = vm.semantic_search("what is my name?", limit=5)
print("SEARCH RESULTS:")
for r in results:
    print(r)
