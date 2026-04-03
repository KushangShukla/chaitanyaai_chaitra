from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
