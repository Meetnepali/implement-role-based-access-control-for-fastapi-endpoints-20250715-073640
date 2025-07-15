from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from functools import wraps
import threading

app = FastAPI(
    title="User Feedback Dashboard API",
    description="API for managing user feedback and admin dashboard operations.",
    version="1.0.0"
)

user_router = APIRouter(prefix="/feedback", tags=["User Feedback"])
admin_router = APIRouter(prefix="/admin", tags=["Admin Feedback Dashboard"])

# In-memory 'DB'
feedback_db: List[Dict[str, Any]] = []
feedback_id_counter = 1
feedback_lock = threading.Lock()

# ---- Schemas ----
class FeedbackIn(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    message: str = Field(..., min_length=10, max_length=1000, example="I really like the new dashboard features!")

class FeedbackOut(BaseModel):
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="user@example.com")
    message: str = Field(..., example="Great app!")

class FeedbackListOut(BaseModel):
    total: int = Field(..., example=50)
    page: int = Field(..., example=1)
    page_size: int = Field(..., example=10)
    feedbacks: List[FeedbackOut] = Field(...)

class FeedbackSubmitResponse(BaseModel):
    success: bool = Field(..., example=True)
    message: str = Field(..., example="Feedback received. Confirmation email sent.")
    feedback: FeedbackOut

# ---- Auth ----
ADMIN_TOKEN = "secret-admin-token"
def get_admin_token(token: str = Query(..., description="Admin token for access. Pass as ?token=...") ):
    if token != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token."
        )
    return True

# ---- Background Task ----
def send_confirmation_email(email: str, message: str):
    # Simulate sending email - just a print
    print(f"Simulated email: Sending confirmation to {email} for feedback: '{message}'")

# ---- User Routes ----
@user_router.post(
    "/submit",
    status_code=201,
    summary="Submit User Feedback",
    response_model=FeedbackSubmitResponse,
    responses={
        201: {
            "description": "Feedback submitted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Feedback received. Confirmation email sent.",
                        "feedback": {
                            "id": 1,
                            "email": "user@example.com",
                            "message": "Great app!"
                        }
                    }
                }
            }
        },
        422: {"description": "Validation Error"}
    },
)
def submit_feedback(feedback: FeedbackIn, background_tasks: BackgroundTasks):
    global feedback_db, feedback_id_counter
    with feedback_lock:
        feedback_record = {
            "id": feedback_id_counter,
            "email": feedback.email,
            "message": feedback.message,
        }
        feedback_db.append(feedback_record)
        feedback_id_counter += 1
    background_tasks.add_task(send_confirmation_email, feedback.email, feedback.message)
    return FeedbackSubmitResponse(
        success=True,
        message="Feedback received. Confirmation email sent.",
        feedback=FeedbackOut(**feedback_record)
    )

# ---- Admin Routes ----
@admin_router.get(
    "/feedbacks",
    summary="Get All User Feedback (Admin Only)",
    response_model=FeedbackListOut,
    responses={
        200: {
            "description": "Paginated list of feedbacks",
            "content": {
                "application/json": {
                    "example": {
                        "total": 2,
                        "page": 1,
                        "page_size": 2,
                        "feedbacks": [
                            {
                                "id": 1,
                                "email": "user1@example.com",
                                "message": "Great experience!"
                            },
                            {
                                "id": 2,
                                "email": "user2@example.com",
                                "message": "I found a bug in the dashboard."
                            }
                        ]
                    }
                }
            }
        },
        401: {"description": "Invalid admin token"},
    },
)
def get_feedbacks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Feedbacks per page (max 50)"),
    email: Optional[EmailStr] = Query(None, description="Filter by user email"),
    token_auth: bool = Depends(get_admin_token),
):
    # Filter by email if provided
    if email:
        filtered = [f for f in feedback_db if f["email"].lower() == email.lower()]
    else:
        filtered = feedback_db[:]
    total = len(filtered)
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated = filtered[start:end]
    return FeedbackListOut(
        total=total,
        page=page,
        page_size=page_size,
        feedbacks=[FeedbackOut(**fb) for fb in paginated]
    )

app.include_router(user_router)
app.include_router(admin_router)

# Error handler for consistent validation error response (not required by FastAPI, shown for robustness)
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )