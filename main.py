from constants.common_imports import *
from api_instances.client_admin import *


def customOpenAPI():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="MindStreaming",
        version="0.0.1",
        description="",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": ""
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/")
def read_root():
    return {"version": "0.0.1", "name": "MindStreaming"}




@app.get("/status")
def check_status():
    try:
        client= BaseDatabaseConnection._initialize_client()
        client.admin.command("ping")
        return {"status": "Ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Database connection error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=12864)
