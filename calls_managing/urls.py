from django.urls import path
from .views import (
    BestAgentView,
    creat_user,
    LoginView,
    AdminRegisterView,
    call_list,
    call_create,
    call_update,
    call_delete,
    agent_list,
    agent_update,
    agent_delete,
    agent_detail,
    user_list,
    user_update,
)

urlpatterns = [
    path("best-agent/", BestAgentView.as_view(), name="best-agent"),
    path("create-user/", creat_user.as_view(), name="create-user"),
    path("agent-login/", LoginView.as_view(), name="agent-login"),
    path("admin-register/", AdminRegisterView.as_view(), name="admin-register"),
    path("admin-login/", LoginView.as_view(), name="admin-login"),
    path("call-list/", call_list.as_view(), name="call-list"),
    path("call-create/", call_create.as_view(), name="create-call"),
    path("call-update/<int:pk>/", call_update.as_view(), name="update-call"),
    path("call-delete/<int:pk>/", call_delete.as_view(), name="delete-call"),
    path("agent-list/", agent_list.as_view(), name="agent-list"),
    path("agent-update/<int:pk>/", agent_update.as_view(), name="update-agent"),
    path("agent-delete/<int:pk>/", agent_delete.as_view(), name="delete-agent"),
    path("agent-detail/<int:pk>/", agent_detail.as_view(), name="detail-agent"),
    path("user-list/", user_list.as_view(), name="user-list"),
    path("user-update/<int:pk>/", user_update.as_view(), name="update-user"),
]
