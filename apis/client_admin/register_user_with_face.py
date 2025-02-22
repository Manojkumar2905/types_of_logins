from starlette import status

from constants.common_imports import *
from fastapi import Form

from constants.response_structure import ResponseUtil

users_collection = ClientConnection.get_collection(settings.CLIENT_DETAILS)

mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.7)
face_mesh = mp_face.FaceMesh(static_image_mode=True, min_detection_confidence=0.7)


# Function to capture an image and process face & hand
def capture_face_hand_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Camera not accessible")

    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise HTTPException(status_code=500, detail="Failed to capture image")

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape  # Get image dimensions
    hand_results = hands.process(frame_rgb)
    face_results = face_mesh.process(frame_rgb)

    if not hand_results.multi_hand_landmarks and not face_results.multi_face_landmarks:
        raise HTTPException(status_code=400, detail="No face or hand detected")

    # Extract hand landmarks
    hand_landmarks = []
    if hand_results.multi_hand_landmarks:
        for landmark in hand_results.multi_hand_landmarks[0].landmark:
            hand_landmarks.append([landmark.x * w, landmark.y * h, landmark.z])

    # Extract face landmarks
    face_landmarks = []
    if face_results.multi_face_landmarks:
        for landmark in face_results.multi_face_landmarks[0].landmark:
            face_landmarks.append([landmark.x * w, landmark.y * h, landmark.z])

    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8"), hand_landmarks, face_landmarks


@app.post("/client_admin/register_with_face",tags=["ClientAdmin"])
async def register_user(username: str = Form(...)):
    image_data, hand_landmarks, face_landmarks = capture_face_hand_image()
    user_id = users_collection.insert_one({
        "username": username,
        "image": image_data,
        "hand_landmarks": json.dumps(hand_landmarks),
        "face_landmarks": json.dumps(face_landmarks)
    }).inserted_id
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ResponseUtil.success_response(
            message="succesfully created user"
        )

    )
