from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.auth import authenticate
from django.contrib.auth.models import User
import psycopg2

class LoginView(TokenObtainPairView):
    pass

@api_view(["GET"])
def dashboard(request):

    user=request.user

    conn=psycopg2.connect(
        dbname="chaitra_db",
        user="postgres",
        password="root64",
        host="localhost",
        port="5432"
    )
    cursor=conn.cursor()

    cursor.execute("""
                SELECT AVG (prediction), COUNT(*)
                FROM query_logs
                WHERE user_id=%s 
                """, (str(user.id),))
    
    avg_pred,total_queries=cursor.fetchone()

    return Response({
        "avg_prediction":avg_pred,
        "total_queries":total_queries
    })

@api_view(["POST"])
def signup(request):
    user=User.objects.create_user(
        username=request.data["email"]
        password=request.data["password"]
    )
    return Response({"message":"User created"})

@api_view(["POST"])
def login(request):
    user=authenticate(
        username=request.data["email"]
        password=request.data["password"]
    )
    if user:
        return Response({"message":"Login success"})
    
    return Response({"error":"Invalid credentials"})