from fastapi import APIRouter, WebSocket, Depends
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, Authorize: AuthJWT = Depends()):
    await websocket.accept()
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close()
        return
    Authorize.jwt_required("websocket", token=token)
    username = Authorize.get_jwt_subject()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Hello {username}, you received a new notification!")
