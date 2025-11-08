from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

class DatabaseService:
    _instance = None
    _client: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance
    
    @property
    def client(self) -> Client:
        return self._client

# Global instance
db = DatabaseService().client
