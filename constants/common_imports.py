from threading import Semaphore
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from database.mongodb_connections import *
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel
from typing import Any, Dict
import uvicorn as uvicorn
from fastapi import HTTPException
from pymongo import MongoClient
from database.mongodb_connections import *
from constants.config import settings
from fastapi import FastAPI, WebSocket
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
import pymongo
import mediapipe as mp
import json
from bson import ObjectId

import cv2
import os
import numpy as np
import mediapipe as mp
import base64
import json
from typing import Dict
import jwt
from datetime import datetime, timedelta
import asyncio
import websockets


MAX_CONCURRENT_CONNECTIONS = 100  # Adjust this number based on system capacity
semaphore = Semaphore(MAX_CONCURRENT_CONNECTIONS)

app = FastAPI(title="MindStreaming", summary="")
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()