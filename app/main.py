import os
import logging
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, Depends, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from bson.objectid import ObjectId
from .database import patient_collection, list_patients
from .schemas import PatientCreate, PatientUpdate, Token, User
from .auth import authenticate_user, create_access_token, get_current_user

app = FastAPI(title="Healthcare Medical Records System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("healthcare_system")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": None})

@app.post("/login")
async def ui_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Invalid username or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/patients", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=3600,
    )
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/patients", response_class=RedirectResponse)
async def create_patient(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    diagnosis: str = Form(...),
    email: str = Form(None),
    notes: str = Form(None),
    current_user: User = Depends(get_current_user),
):
    patient_data = {
        "name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "email": email,
        "notes": notes,
        "created_at": datetime.utcnow(),
    }
    result = await patient_collection.insert_one(patient_data)
    logger.info("Created patient %s", result.inserted_id)
    return RedirectResponse(url="/patients", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/patients", response_class=HTMLResponse)
async def read_patients(request: Request, current_user: User = Depends(get_current_user)):
    patients = await list_patients()
    for patient in patients:
        patient["id"] = str(patient["_id"])
    return templates.TemplateResponse(
        "patients.html",
        {"request": request, "patients": patients, "user": current_user},
    )

@app.post("/patients/update/{patient_id}", response_class=RedirectResponse)
async def update_patient(
    patient_id: str,
    name: str = Form(None),
    age: int = Form(None),
    gender: str = Form(None),
    diagnosis: str = Form(None),
    email: str = Form(None),
    notes: str = Form(None),
    current_user: User = Depends(get_current_user),
):
    update_data = {k: v for k, v in {
        "name": name,
        "age": age,
        "gender": gender,
        "diagnosis": diagnosis,
        "email": email,
        "notes": notes,
    }.items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    result = await patient_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    logger.info("Updated patient %s by %s", patient_id, current_user.username)
    return RedirectResponse(url="/patients", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/patients/delete/{patient_id}")
async def delete_patient(patient_id: str, current_user: User = Depends(get_current_user)):
    result = await patient_collection.delete_one({"_id": ObjectId(patient_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    logger.info("Deleted patient %s by %s", patient_id, current_user.username)
    return {"message": "Patient deleted successfully"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
