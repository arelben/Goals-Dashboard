import os
from supabase import create_client, Client
from dotenv import load_dotenv

def test_connection():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print(f"Testing connection to: {url}")
    
    try:
        supabase: Client = create_client(url, key)
        # Intentamos una consulta simple a la tabla 'goals'
        response = supabase.table("goals").select("count", count="exact").execute()
        print("✅ Connection successful!")
        print(f"Current rows in 'goals': {response.count}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
