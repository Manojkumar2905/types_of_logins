from constants.common_imports import *
from apis.client_admin.register_user_with_face import *


@app.post("/client_admin/verify_user",tags=["ClientAdmin"])
async def verify_user(username: str = Form(...)):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    captured_image, captured_hand_landmarks, captured_face_landmarks = capture_face_hand_image()
    stored_hand_landmarks = json.loads(user["hand_landmarks"])
    stored_face_landmarks = json.loads(user["face_landmarks"])

    # Convert to NumPy arrays for numerical comparison
    captured_hand_landmarks = np.array(captured_hand_landmarks)
    stored_hand_landmarks = np.array(stored_hand_landmarks)
    captured_face_landmarks = np.array(captured_face_landmarks)
    stored_face_landmarks = np.array(stored_face_landmarks)

    # Adjusted threshold to allow similar matches
    hand_diff = np.linalg.norm(captured_hand_landmarks - stored_hand_landmarks)
    face_diff = np.linalg.norm(captured_face_landmarks - stored_face_landmarks)

    if hand_diff < 100 and face_diff < 100:  # Looser threshold for verification
        return JSONResponse(content={"message": "Login successful"})
    else:
        return JSONResponse(content={"message": "Failed to login"})