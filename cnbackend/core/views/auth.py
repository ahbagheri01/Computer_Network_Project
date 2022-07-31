from rest_framework.views import APIView

class LoginView(APIView):
    http_method_names = ['post']

    def post(self, request):
        username = request.username
        password = request.password
        