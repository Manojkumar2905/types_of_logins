from starlette import status
from starlette.responses import JSONResponse

from constants.common_imports import *
from constants.response_structure import ResponseUtil


class ClientDetails(BaseModel):
    clientname:str
    email:str
    mobile:str
    user_name:str
    password:str


@app.post("/client_admin/create_user", tags=["ClientAdmin"])
async def create_user(request: Request, response: Response, item: ClientDetails):
    try:
        data={
            "clientname": item.name,
            "clientemail": item.email,
            "clientmobile": item.mobile,
            "user_name": item.user_name,
            "password": item.password
        }
        client_db= ClientConnection.get_collection(settings.CLIENT_DETAILS)
        details=client_db.insert_one(data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ResponseUtil.success_response(
                message="succesfully created user"
            )

        )


    except Exception as e:
        return e
