from fastapi import FastAPI, openapi,Header,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from usuario import userInfo, createNewUser, loginUser, updateUser
from pacientes import getAllPatients, AddNewPatient, FindPatientInDb, updatePatient
from consultas import addConsults, FindConsultById, updateConsult, FindAllConsults
from reportes import FindAReport
from entidades import Usuario,Paciente,Consulta,UsuarioClave, Token

from datetime import date

from util import tokenTime

app = FastAPI(
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

#----------------Usuario-----------------
@app.post("/api/createUser", tags=["USER"])
def CreateUser(user:UsuarioClave):
    return createNewUser(user)

@app.post("/api/login",tags=["USER"] )
def Login(user:UsuarioClave):
    return loginUser(user)

@app.put("/api/users", tags=["USER"])
def ChangeInfo(user:UsuarioClave, token: str = Header(None)):
    return updateUser(user)

@app.get("/api/users/{Id}", tags=["USER"])
def Info(Id:int, token: str = Header(None)):
    if tokenTime(token, Id):
        return userInfo(Id)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

#-------------------Paciente--------------
@app.get("/api/patients", tags=["Patient"])
def Patients(uid: int, token: str = Header(None) ):
    if tokenTime(token, uid):
        return getAllPatients(uid)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.post("/api/patients", tags=["Patient"])
def AddPatients(patient:Paciente, uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return AddNewPatient(patient)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.get("/api/patients/{Id}", tags=["Patient"])
def FindPatient(Id:int, uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return FindPatientInDb(Id)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.put("/api/patients/", tags=["Patient"])
def ModifyPatient(patient:Paciente,uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return updatePatient(patient, uid)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

#----------------------Consults-----------------------
@app.post("/api/consults", tags=["Consult"])
def Consults(consults:Consulta, uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return addConsults(consults, uid)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.get("/api/consults", tags=["Consult"])
def FindConsult(uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return FindAllConsults(uid)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.get("/api/consults/{cid}", tags=["Consult"])
def FindOneConsultById(cid: int, uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return FindConsultById(cid, uid)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

@app.put("/api/consults/{paciente}", tags=["Consult"])
def ModifyConsult(consults:Consulta, paciente:int, uid: int, token: str = Header(None)):
    if tokenTime(token, uid):
        return updateConsult(consults, paciente)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }

#----------------------Resports-------------------
@app.get("/api/reports", tags=["Reports"])
def FindReport(opcion:int, uid: int, fecha: Optional[date] = None, token: str = Header(None)):
    if tokenTime(token, uid):
        return FindAReport(opcion, uid, fecha)
    else: 
        return {
            "status": False, "message": "Usuario No Valido"
        }