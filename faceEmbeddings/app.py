# app.py - Clean Face Recognition API for Attendance System
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import base64
import cv2
import numpy as np
import time
import io
from insightface.app import FaceAnalysis
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ==================== MODEL LOADING ====================

FACE_ANALYSIS_AVAILABLE = False
YOLO_MODEL_AVAILABLE = False
yolo_model = None
face_app = None
SIMILARITY_THRESHOLD = 0.5  # Configurable threshold

try:
    # Load YOLOv5 model for face detection
    from ultralytics import YOLO
    try:
        # Load your trained YOLOv5 face detection model
        yolo_model = YOLO("classeye.pt")  # Change to your model path
        YOLO_MODEL_AVAILABLE = True
        logger.info("✅ YOLOv5 model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load YOLO model: {e}")
        YOLO_MODEL_AVAILABLE = False
    
    # Load InsightFace for face recognition (embeddings)
    face_app = FaceAnalysis(name="buffalo_l")
    face_app.prepare(ctx_id=-1, det_size=(640, 640))  # CPU mode
    FACE_ANALYSIS_AVAILABLE = True
    logger.info("✅ InsightFace loaded successfully")
    
except Exception as e:
    logger.error(f"❌ Error loading models: {e}")
    raise Exception("Failed to load required models")

# ==================== PYDANTIC MODELS ====================

class StudentData(BaseModel):
    studentId: str
    name: str
    roll_no: Optional[str] = ""
    embedding: List[float]

class GenerateEmbeddingsRequest(BaseModel):
    student_id: str
    student_name: str
    images: List[str]

class RecognizeRequest(BaseModel):
    images: List[str]
    students: List[StudentData]

# ==================== HELPER FUNCTIONS ====================

def base64_to_cv2_image(b64_string: str):
    """Convert base64 to OpenCV image"""
    try:
        if b64_string.startswith('data:'):
            b64_string = b64_string.split(',')[1]
        
        img_data = base64.b64decode(b64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        return None

def calculate_average_embedding(embeddings_list):
    """Calculate average embedding from list of embeddings"""
    if not embeddings_list:
        return None
    embeddings_array = np.array(embeddings_list)
    avg_embedding = np.mean(embeddings_array, axis=0)
    return avg_embedding.tolist()

def detect_faces_yolo(image):
    """Detect faces using YOLOv5"""
    faces = []
    try:
        results = yolo_model(image)
        for result in results:
            if result.boxes is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                
                for i, box in enumerate(boxes):
                    x1, y1, x2, y2 = map(int, box)
                    faces.append({
                        "bbox": [x1, y1, x2, y2],
                        "confidence": float(confidences[i]) if i < len(confidences) else 0.5
                    })
        return faces
    except Exception as e:
        logger.error(f"YOLO detection error: {e}")
        return []

def crop_face(image, bbox):
    """Crop face from image using bounding box"""
    x1, y1, x2, y2 = bbox
    h, w = image.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    
    if x2 <= x1 or y2 <= y1:
        return None
    
    return image[y1:y2, x1:x2]

def get_face_embedding(face_crop):
    """Extract face embedding using InsightFace"""
    try:
        faces = face_app.get(face_crop)
        if len(faces) == 0:
            return None
        return faces[0].embedding.tolist()
    except Exception as e:
        logger.error(f"Embedding extraction error: {e}")
        return None

def match_embedding(embedding, students):
    """Match embedding with student embeddings using cosine similarity"""
    if not embedding or not students:
        return None, 0.0
    
    try:
        query_embedding = np.array(embedding).reshape(1, -1)
        student_embeddings = np.array([s.embedding for s in students])
        
        similarities = cosine_similarity(query_embedding, student_embeddings)[0]
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]
        
        if best_similarity >= SIMILARITY_THRESHOLD:
            return students[best_idx], float(best_similarity)
        return None, best_similarity
    except Exception as e:
        logger.error(f"Similarity matching error: {e}")
        return None, 0.0

# ==================== ENDPOINTS ====================

@app.post("/generate-embeddings")
async def generate_embeddings(payload: GenerateEmbeddingsRequest):
    """Generate face embeddings from multiple images"""
    start_time = time.time()
    all_embeddings = []
    
    for idx, img_str in enumerate(payload.images):
        img = base64_to_cv2_image(img_str)
        if img is None:
            continue
        
        faces = face_app.get(img)
        if len(faces) > 0:
            all_embeddings.append(faces[0].embedding.tolist())
            logger.info(f"Image {idx + 1}: Face detected")
    
    if len(all_embeddings) < 3:
        return {
            "success": False,
            "message": f"Need at least 3 face images, got {len(all_embeddings)}"
        }
    
    average_embedding = calculate_average_embedding(all_embeddings)
    
    return {
        "success": True,
        "embeddings": average_embedding,
        "face_detected": True,
        "confidence": 0.95,
        "processing_time": round(time.time() - start_time, 3),
        "embedding_dimension": len(average_embedding),
        "images_processed": len(payload.images),
        "valid_embeddings_count": len(all_embeddings),
        "message": f"Generated embeddings from {len(all_embeddings)} images"
    }

@app.post("/recognize")
async def recognize_faces(payload: RecognizeRequest):
    """
    Face recognition for attendance marking
    
    Steps:
    1. Accepts base64 images
    2. Accepts students with embeddings
    3. Uses YOLOv5 for face detection
    4. Crops detected faces
    5. Uses InsightFace for embeddings
    6. Compares with student embeddings
    7. Returns recognized students
    """
    start_time = time.time()
    
    if not payload.images or not payload.students:
        raise HTTPException(status_code=400, detail="Images and students required")
    
    if not YOLO_MODEL_AVAILABLE or not FACE_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=500, detail="Face recognition models not available")
    
    recognized_students = []
    total_faces_detected = 0
    
    for img_idx, img_b64 in enumerate(payload.images):
        image = base64_to_cv2_image(img_b64)
        if image is None:
            continue
        
        # Detect faces with YOLOv5
        faces = detect_faces_yolo(image)
        total_faces_detected += len(faces)
        
        for face in faces:
            bbox = face["bbox"]
            detection_conf = face["confidence"]
            
            # Crop face
            face_crop = crop_face(image, bbox)
            if face_crop is None:
                continue
            
            # Get embedding
            embedding = get_face_embedding(face_crop)
            if embedding is None:
                continue
            
            # Match with students
            student, similarity = match_embedding(embedding, payload.students)
            if student:
                # Calculate overall confidence
                confidence = detection_conf * similarity
                
                # Check if already recognized
                existing = next((s for s in recognized_students if s["studentId"] == student.studentId), None)
                if existing:
                    if confidence > existing["confidence"]:
                        existing["confidence"] = confidence
                        existing["bbox"] = bbox
                else:
                    recognized_students.append({
                        "studentId": student.studentId,
                        "name": student.name,
                        "roll_no": student.roll_no,
                        "confidence": confidence,
                        "bbox": bbox,
                        "detection_confidence": detection_conf,
                        "similarity_score": similarity
                    })
    
    processing_time = round(time.time() - start_time, 3)
    
    return {
        "success": True,
        "recognized": recognized_students,
        "total_faces_detected": total_faces_detected,
        "processing_time": processing_time,
        "timestamp": datetime.now().isoformat(),
        "images_processed": len(payload.images),
        "recognition_rate": round((len(recognized_students) / len(payload.students)) * 100, 2) 
                        if len(payload.students) > 0 else 0
    }

@app.get("/health")
async def health_check():
    return {
        "success": True,
        "yolo_available": YOLO_MODEL_AVAILABLE,
        "insightface_available": FACE_ANALYSIS_AVAILABLE,
        "similarity_threshold": SIMILARITY_THRESHOLD
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#uvicorn app:app --reload --port 8000