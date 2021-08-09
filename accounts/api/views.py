from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from accounts.api.serializers import RegistrationSerializer

@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['id'] = account.id
            data['response'] = 'successfully registered a new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['status'] = 'success'
        else:
            errorKeys = list(serializer.errors.keys())
            if 'email' in errorKeys:
                data['message'] = serializer.errors['email'][0].capitalize()
            elif 'username' in errorKeys:
                data['message'] = serializer.errors['username'][0].capitalize()
            elif 'password' in errorKeys:
                data['message'] = serializer.errors['password'][0].capitalize()
            data['status'] = 'failed'
        
        return Response(data)




class loginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username,
            'email': user.email
        })
        


class logoutView(APIView):
    def post(self, request, format=None):
        try:
            authorization = request.META.get('HTTP_AUTHORIZATION')
            token = authorization.split()[1]
            user = Token.objects.get(key=token).user
            # delete the token
            user.auth_token.delete()
        except:
            pass
        return Response({"message":"logged out successfully", "status":status.HTTP_200_OK})

# class AccountViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = RegistrationSerializer

# def get_csrf(request):
#     response = JsonResponse({"Info": "Success - Set CSRF cookie"})
#     response["X-CSRFToken"] = get_token(request)
#     return response

# @require_POST
# def loginView(request):
#     data = json.loads(request.body)
#     email = data.get("email")
#     password = data.get("password")

#     if email is None or password is None:
#         return JsonResponse({"info": "Email and Password is needed"})

#     user = authenticate(request, email=email, password=password)
#     if user is None:
#         return JsonResponse({"info": "User does not exist"}, status=400)

#     login(request, user)
#     return JsonResponse({"info": "User logged in successfully", "username": user.username})

# @login_required
# def logoutView(request):
#     logout(request)
#     return JsonResponse({"info": "User logged out successfully"})


# class WhoAmIView(APIView):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]

#     @staticmethod
#     def get(request, format=None):
#         if request.user.is_authenticated:
#             return JsonResponse({"username": request.user.get_username()})