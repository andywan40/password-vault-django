from .serializers import PasswordSerializer
from password.models import Password
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
# from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import api_view


class PasswordViewSet(viewsets.ModelViewSet):
    authentication_classes = [ TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = PasswordSerializer

    def get_queryset(self):
        user = self.request.user
        user_id = user.id
        type = self.request.query_params["type"]
        if type == "favorite":
            return Password.objects.all().filter(account=user_id, is_favorite=True)
        if type == "all":
            return Password.objects.all().filter(account=user_id)
        
        return Password.objects.all().filter(account=user_id)
    
    def create(self, request):
        user_id = request.user.id
        data = request.data
        data['account'] = user_id
        serializer = PasswordSerializer(data=data)
        response_data = {}
        if serializer.is_valid():
            serializer.save()
            response_data['message'] = 'successfully created a password'
            response_data['status'] = status.HTTP_201_CREATED
            response_data['data'] = serializer.data
        else:
            errorKeys = list(serializer.errors.keys())
            response_data['message'] = 'failed to create a password'
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['errors'] = errorKeys
        
        return Response(response_data)

    def update(self, request, pk):
        instance = Password.objects.get(pk=pk)
        serializer = PasswordSerializer(instance, data=request.data, partial=True)
        response_data = {}
        if serializer.is_valid():
            serializer.save()
            response_data['message'] = 'successfully updated the password'
            response_data['status'] = status.HTTP_200_OK
            response_data['data'] = serializer.data
        else:
            errorKeys = list(serializer.errors.keys())
            response_data['message'] = 'failed to update the password'
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['errors'] = errorKeys
        return Response(response_data)
    
    def destroy(self, request, pk):
        password = Password.objects.get(pk=pk)
        try:
            password.delete()
            return Response({"status": status.HTTP_200_OK})
        except:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

    @action(detail=False, methods=["post"])
    def destroymultiple(self, request):
        user = self.request.user
        user_id = user.id
        ids = request.data["ids"]
        error = False
        for id in ids:
            try:
                password = Password.objects.all().filter(account=user_id, id=id)
                password.delete()
            except:
                error = True
        
        if error:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "message": "failed to delete the passwords"})    
        return Response({"status": status.HTTP_200_OK, "message": "successfully deleted the passwords"})

# @api_view(['GET', 'POST',])
# def password_list(request):
#     #get all password items (we will not use this)
#     if request.method == "GET":
#         passwords = Password.objects.all()
#         #passwords = Password.objects.all().filter(account=1)
#         serializer = PasswordSerializer(passwords, many=True)
#         return Response(serializer.data)
#         #return Response({"passwords": serializer.data})

#     #create a new password item
#     elif request.method == "POST":
#         serializer = PasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# @api_view(['GET', 'PUT', 'DELETE',])
# def password_detail(request, pk):
#     try:
#         password = Password.objects.get(pk=pk)
#     except Password.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     # get details of a password item
#     if request.method == "GET":
#         serializer = PasswordSerializer(password)
#         return Response(serializer.data)
    
#     # update details of a password item
#     elif request.method == "PUT":
#         serializer = PasswordSerializer(password, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     #delete a password item
#     elif request.method == "DELETE":
#         password.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)