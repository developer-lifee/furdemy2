import os
from supabase import create_client

# Asegúrate de que estas sean las credenciales correctas y trata de no exponer tu key públicamente
url = "https://hmyuqiqxliywqtsjuhfj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhteXVxaXF4bGl5d3F0c2p1aGZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE5MTMyNjEsImV4cCI6MjAyNzQ4OTI2MX0.ueFGs__gDmkICQohhHkONSiU0aTeaMDipdMW1VBV9_o"

supabase = create_client(url, key)

response = supabase.table('usuarios').select('*').execute()

