from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status
from .models import Administrator, call, User
from .serializer import (
    AgentSerializer,
    call_serializer,
    User_serializer,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BestAgentView(APIView):
    def post(self, request):
        phone_number = request.data.get(
            "phone_number"
        )  # Assuming phone number is sent in the request       location = request.data.get("location")
        language = request.data.get("language")
        age = request.data.get("age")

        agents = Administrator.objects.filter(phone_numbers__contains=[phone_number])

        # Step 2: Order agents based on rating
        agents_lang_ranked = agents.order_by("-rating")

        if agents_lang_ranked:
            # Step 2: If user has called before, find the agent they spoke with

            agent = agents_lang_ranked.first()
            if agent:
                # Serialize the agent data
                serializer = AgentSerializer(agent)
                return Response(
                    {
                        "message": "Returning to the same agent",
                        "agent": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
        if not agents_lang_ranked:
            agents_with_language = Administrator.objects.filter(
                first_prefered_language=language, on_duty=True
            )
            agents_lang_ranked = agents_with_language.order_by("-rating")
            agent = agents_lang_ranked.first()
            serializer = AgentSerializer(agent)
            if agent:
                agent = Administrator.objects.filter(
                    first_prefered_language=language, age=age
                )
                agents_with_lan_and_age = Administrator.objects.filter(
                    language=language, age=age, on_duty=True
                )
                Lan_and_age_agents_ranked = agent.objects.filter(
                    call__in=agents_with_lan_and_age, on_duty=True
                ).order_by("-rating")
                agent_with_lan_and_age = Lan_and_age_agents_ranked.first()
                agent_with_lan_and_age_serializer = AgentSerializer(
                    agent_with_lan_and_age
                )
                if not agent_with_lan_and_age:
                    return Response(
                        {
                            "message": "New agent assigned based on language",
                            "agent": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {
                            "message": "New agent assigned based on language and age",
                            "agent": agent_with_lan_and_age_serializer,
                        },
                        status=status.HTTP_200_OK,
                    )
            if not agent:
                agent = Administrator.objects.filter(age=age, on_duty=True).first()
                if agent:
                    serializer = AgentSerializer(agent)
                    return Response(
                        {
                            "message": "New agent assigned based on age",
                            "agent": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                if not agent:
                    agent = Administrator.objects.filter(
                        first_prefered_language=language, on_duty=True
                    ).first()
                    serialized_agent = AgentSerializer(agent)
                    if serialized_agent:
                        return Response(
                            {
                                "message": "No suitable agent found , sending the first availlable one",
                                "agent": serialized_agent.data,
                            },
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    else:
                        return Response(
                            {"message": "No suitable agent found "},
                            status=status.HTTP_404_NOT_FOUND,
                        )


""" agents logic """

from rest_framework.permissions import BasePermission


class agent_list(generics.ListAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class agent_update(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class agent_delete(generics.DestroyAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class agent_detail(generics.RetrieveAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


"""users logic"""


class creat_user(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = User_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class user_list(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = User_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class user_update(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = User_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


""" adding new agent and agent login logic """


@authentication_classes([])
@permission_classes([])
class AdminRegisterView(APIView):
    def post(self, request):
        serializer = AgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


@authentication_classes([])
@permission_classes([])
class LoginView(APIView):
    def post(self, request):

        password = request.data.get("password")
        username = request.data.get("username")
        user = Administrator.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        response.set_cookie(key="jwt", value=access_token, httponly=True)
        response.data = {"jwt": access_token, "message": "success"}

        return response


""" calls logic """


class call_list(generics.ListAPIView):
    queryset = call.objects.all()
    serializer_class = call_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class call_update(generics.RetrieveUpdateDestroyAPIView):
    queryset = call.objects.all()
    serializer_class = call_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class call_create(generics.CreateAPIView):
    queryset = call.objects.all()
    serializer_class = call_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class call_delete(generics.DestroyAPIView):
    queryset = call.objects.all()
    serializer_class = call_serializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
