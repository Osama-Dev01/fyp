# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware

# from filters import validate_tweet

# app = FastAPI()



# # Allow CORS (for Chrome extension to communicate)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For testing, restrict in production
#     allow_methods=["POST"],
#     allow_headers=["*"],
    
# )



# @app.post("/receive-tweet")
# async def classify_tweet_endpoint(request: Request):
#     """
#     Endpoint to receive a tweet, validate it using the filtering pipeline,
#     and (later) pass it to the ML model for classification.
#     """
#     data = await request.json()
#     tweet_text = data.get("tweet_text")

#     if not tweet_text:
#         return {"status": "error", "message": "No tweet_text provided."}

#     print(f"Received tweet for validation: '{tweet_text}'")

#     # --- Use the imported validation function ---
#     is_valid, reason = validate_tweet(tweet_text)

#     # --- If the tweet is NOT valid, return immediately ---
#     if not is_valid:
#         print(f"-> Tweet REJECTED. Reason: {reason}")
#         # This response goes directly back to your Chrome plugin
#         return {"status": "not_valid", "message": reason}

#     # --- If the tweet IS valid, proceed ---
#     print(f"-> Tweet PASSED validation. Ready for classification.")
    
#     #
#     # TODO: Add your ML model classification logic here
#     # For now, we'll just return a success message.
#     #
#     # example_prediction = classifier(tweet_text) 
#     #
    
#     return {
#         "status": "success",
#         "message": "Tweet passed validation and is ready for classification."
#         # In the future, you'll add the model's output here:
#         # "predicted_label": example_prediction['label'],
#         # "confidence_score": example_prediction['score']
#     }






# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# main.py
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import User, ApprovalStatus
from database import engine, get_db, Base
from filters import validate_tweet
from admin.admin_routes import router as admin_router
from member.member_routes import router as member_router

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include routers
app.include_router(admin_router)
app.include_router(member_router)










        

if __name__ == "__main__":
    import uvicorn
    # Changed from 0.0.0.0 to localhost (127.0.0.1)
    uvicorn.run(app, host="127.0.0.1", port=8000)










































# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel  # Add this import
# from sqlalchemy.orm import Session
# from models import User, ApprovalStatus
# from database import engine, get_db, Base
# from fastapi.middleware.cors import CORSMiddleware
# # Add this Pydantic model
# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#     role: str

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # CORS middleware remains the same
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Update your endpoint to use the Pydantic model
# @app.post("/users/")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     if user.role not in ["admin", "member"]:
#         raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'member'")
    
#     db_user = User(
#         username=user.username,
#         email=user.email,
#         password=user.password,
#         role=user.role,
#         approval_status=ApprovalStatus.approved.value if user.role == "admin" else ApprovalStatus.pending.value
#     )
    
#     try:
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return {"message": "User created successfully", "user_id": db_user.user_id}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)