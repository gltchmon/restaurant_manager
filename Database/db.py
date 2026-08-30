from supabase import create_client, Client
from supabase.client import ClientOptions
from dotenv import load_dotenv
import os
import csv
from decimal import Decimal
import httpx
from supabase.lib.client_options import SyncClientOptions

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

c_http_client  = httpx.Client(timeout=httpx.Timeout(60.0,read=60.0))
options  = SyncClientOptions(httpx_client=c_http_client)

supabase: Client = create_client(url,key, options=options)


    