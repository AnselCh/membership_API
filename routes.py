from datetime import datetime
from fastapi import APIRouter, Body, Depends, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Member, MemberUpdate, Login
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uuid import uuid4
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

router = APIRouter()
security = HTTPBasic()


@router.post("/", response_description="Create a new account", status_code=status.HTTP_201_CREATED, response_model=Member)
def create_member(request: Request, member: Member = Body(...)):
    # 檢查帳號是否已存在
    existing_member = request.app.database["member_data"].find_one(
        {"account": member.account}
    )
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")

    # 新增會員
    member = jsonable_encoder(member)
    new_member = request.app.database["member_data"].insert_one(member)
    created_member = request.app.database["member_data"].find_one(
        {"_id": new_member.inserted_id}
    )

    # 加上時間戳記
    created_member["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return created_member


@router.get("/", response_description="List all member", response_model=List[Member])
def list_memberships(request: Request):
    members = list(request.app.database["member_data"].find(limit=100))

    # 加上時間戳記
    for member in members:
        member["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return members


@router.get("/{account}", response_description="Get member by id", response_model=Member)
def find_member(account: str, request: Request):
    if (member := request.app.database["member_data"].find_one({"account": account})) is not None:

        # 加上時間戳記
        member["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return member

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Member with account {account} not found")


@router.patch("/{account}", response_description="Update member info", response_model=Member)
def update_member(account: str, request: Request, member: MemberUpdate = Body(...)):
    member = {k: v for k, v in member.dict().items() if v is not None}

    if len(member) >= 1:
        update_result = request.app.database["member_data"].update_one(
            {"account": account}, {"$set": member}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with ID {account} not found")

    if (
        existing_book := request.app.database["member_data"].find_one({"account": account})
    ) is not None:

        # 加上時間戳記
        existing_book["timestamp"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Member with ID {account} not found")


@router.delete("/{account}", response_description="Delete account")
def delete_member(account: str, request: Request, response: Response):
    delete_result = request.app.database["member_data"].delete_one(
        {"account": account})

    if delete_result.deleted_count == 1:
        response.headers["timestamp"] = str(datetime.now())
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Member with ID {account} not found")


@router.post("/login")
def login(request: Request, account: str = Body(...), password: str = Body(...)):
    # 檢查帳號密碼是否正確
    member_data = request.app.database["member_data"]
    member = member_data.find_one(
        {"account": account, "password": password}, {'_id': 0})
    if not member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect account or password")

    elif account == 'iamadmin':
        return {
            "msg": 'admin'
        }

    # 加上時間戳記
    # member["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # return member


"""
@router.post("/login")
def login(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 檢查帳號密碼是否正確
    member = request.app.database["member_data"].find_one(
        {"account": credentials.username, "password": credentials.password}, {'_id': 0})
    if member is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect account or password")

    # 加上時間戳記
    member["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return member
"""
