"""
This module contains the account controller. It defines the routes for account-related operations
such as login, registration, and profile retrieval. The controller interacts with the account service
to handle business logic and data operations.
"""

from flask import Blueprint, request
from dependify import inject

from account.application.account_service import AccountService
from account.application.token_service import TokenService
from .dto import AccountDto, RegisterDto, LoginDto

controller = Blueprint("account", __name__, url_prefix="/accounts")


@controller.post("/login")
@inject
def login(account_service: AccountService, token_service: TokenService):
    data = LoginDto(**request.json)  # validate the request data
    account = account_service.authenticate(data)
    token = token_service.create_access_token(account)
    return {"access_token": token, "token_type": "bearer"}


@controller.post("/register")
@inject
def register(account_service: AccountService):
    data = RegisterDto(**request.json)  # validate the request data
    account = account_service.create_account(data)
    return AccountDto.new(account).model_dump()


@controller.get("/profile")
@inject
def profile(account_service: AccountService):
    # Get the current user ID from the application context
    # This requires authentication middleware to be set up
    user_id = account_service.app_context.identity()
    account = account_service.get_account(user_id)
    return AccountDto.new(account).model_dump()
