import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.memory.conversation_history_service import ConversationHistoryService
import time

print("Testing conversation history service...")
hs = ConversationHistoryService()
hs.add_message("user", "Testing embedding generation and storage.")
print("Message added. Waiting for background thread to complete...")
time.sleep(5)
print("Done.")
