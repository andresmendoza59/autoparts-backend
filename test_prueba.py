from pymongo import MongoClient

uri = "mongodb+srv://Eritz:1234@cluster0.qlydufw.mongodb.net/autoparts_db?retryWrites=true&w=majority"
client = MongoClient(uri)

try:
    print(client.list_database_names())
except Exception as e:
    print("Error de conexión:", e)



"""from users.models import User

user = User.objects.create(
    name="Prueba Usuario",
    email="prueba@example.com",
    password="clave123",  # Puedes aplicar hashing si lo usarás para login
    role="vendedor"
)

print(user)
"""