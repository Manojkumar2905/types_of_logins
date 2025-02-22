import functools
import jwt
from fastapi import HTTPException
from starlette.requests import Request

from constants.config import settings


def web_request_authenticator(f):
    @functools.wraps(f)
    async def decorator(request: Request, *args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"]
        if not token:
            raise HTTPException(status_code=401, detail='a valid token is missing')

        tokenSepration = token.split(" ")
        basicAuthToken = tokenSepration[1]

        try:
            jwt.decode(basicAuthToken, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as error:
            raise HTTPException(status_code=401, detail='token is invalid')
        return await f(request, *args, **kwargs)

        # userInput = stringBytes.get("inputType")
        # databaseUserName = UserConnection.fetch_user_data(userInput)
        # for x in databaseUserName["products"]:
        #     if x["product"] == "fund_manager":
        #         if (userInput == databaseUserName["email"] or
        #             userInput == databaseUserName["contactNumber"] or
        #             userInput == databaseUserName["userName"]) and x["access"] == True:
        #             return await f(*args, databaseUserName["userName"], **kwargs)
        # else:
        #     raise HTTPException(status_code=401, detail='token is invalid')

    return decorator