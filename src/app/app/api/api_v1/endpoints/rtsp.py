import os
from typing import Any
import ffmpeg

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep

from src.app.app.models import RtspUrlOut, RtspUrl
from src.app.app.schemas.rtsp import RtspUrlCreate, RtspUrlUpdate

router = APIRouter()


router.get("/", response_model=list[RtspUrlOut])
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
def convert_rtsp_to_hls(
    *, session: SessionDep, current_user: CurrentUser, item_in: RtspUrlCreate
) -> Any:
    try:
        # Logging the API call to the database
        api_log = RtspUrl.from_orm(item_in, update={"owner_id": current_user.id})
        session.add(api_log)
        session.commit()
        session.refresh(api_log)

        # Converting RTSP to HLS using ffmpeg
        output_directory = f"/path/to/hls/{api_log.id}/"
        os.makedirs(output_directory, exist_ok=True)

        # Using ffmpeg python library to convert RTSP to HLS
        ffmpeg.input(item_in.rtsp_url).output(f"{output_directory}index.m3u8").run()

        # Providing the HLS URL in the response
        hls_url = f"/hls/{api_log.id}/index.m3u8"
        return {"hls_url": hls_url}

    except Exception as e:
        # Handling exceptions appropriately (e.g., log the error)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

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

