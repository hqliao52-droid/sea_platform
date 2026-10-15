from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.crud.sea_data_base import BaseCRUD
from app.models.user_profiles import UserProfile

class UserProfileCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(model=UserProfile)


    async def append_profiles(
            self,
            db: AsyncSession,
            user_id: int,
            profile: str
        ) -> Optional[UserProfile]:
        stmt = (
            select(UserProfile)
            .where(UserProfile.user_id == user_id)
            .with_for_update()          # 加行锁，防并发丢更新
        )
        result = await db.execute(stmt)
        user_profile = result.scalar_one_or_none()

        if user_profile is None:
            # 如果改用户画像不存在，在创建
            user_profile = UserProfile(
                user_id=user_id,
                metadata_={
                    "data": [{
                        "datetime": datetime.now().isoformat(),
                        "profile":"-"
                    }]},
            )
            db.add(user_profile)

        if "-" == user_profile.metadata_["data"][0].get("profile",""):
            user_profile.metadata_["data"][0]["profile"] = profile
        else:
            profile_dict = {"datetime": datetime.now().isoformat(), "profile": profile}
            user_profile.metadata_["data"].append(profile_dict)

        await db.flush()
        await db.refresh(user_profile)
        return user_profile