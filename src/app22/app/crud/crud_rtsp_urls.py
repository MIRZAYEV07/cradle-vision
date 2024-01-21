from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import RtspUrl
from schemas.rtsp_urls import RtspUrlCreate, RtspUrlUpdate


class CRUDItem(CRUDBase[RtspUrl, RtspUrlCreate, RtspUrlUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: RtspUrlCreate, owner_id: int
    ) -> RtspUrl:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[RtspUrl]:
        return (
            db.query(self.model)
            .filter(RtspUrl.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


item = CRUDItem(RtspUrl)
