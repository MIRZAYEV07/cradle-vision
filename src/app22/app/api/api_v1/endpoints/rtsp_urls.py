from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.app22 import CurrentUser, SessionDep
from src.app22 import RtspUrl, RtspUrlCreate, RtspUrlOut, RtspUrlUpdate

router = APIRouter()


@router.get("/", response_model=list[RtspUrlOut])
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve rtsp urls.
    """

    if current_user.is_superuser:
        statement = select(RtspUrl).offset(skip).limit(limit)
        return session.exec(statement).all()
    else:
        statement = (
            select(RtspUrl)
            .where(RtspUrl.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()


@router.get("/{id}", response_model=RtspUrl)
def read_item(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get rtsp urls by ID.
    """
    item = session.get(RtspUrl, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=RtspUrl)
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: RtspUrlCreate
) -> Any:
    """
    Create new rtsp_urls
    """
    item = RtspUrl.from_orm(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}", response_model=RtspUrlOut)
def update_item(
    *, session: SessionDep, current_user: CurrentUser, id: int, item_in: RtspUrlUpdate
) -> Any:
    """
    Update an rtsp_urls.
    """
    item = session.get(RtspUrl, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    # TODO: check this actually works
    update_dict = item_in.dict(exclude_unset=True)
    item.from_orm(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{id}", response_model=RtspUrlOut)
def delete_item(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Delete an rtsp_urls.
    """
    item = session.get(RtspUrl, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item)
    session.commit()
    return item
