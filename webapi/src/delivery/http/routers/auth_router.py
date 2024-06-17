"""
Router for the /auth path. Contains all routes for the router.
"""

from fastapi import APIRouter, status


router = APIRouter(prefix="/auth")


@router.post("/login", status_code=status.HTTP_201_CREATED)
def login():
    return {"status": "logged in"}


@router.delete("/logout", status_code=status.HTTP_200_OK)
def logout():
    return {"message": "Successfully logged out"}
