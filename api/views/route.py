from fastapi import APIRouter,Request,BackgroundTasks
from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import tasks
from db_session import database_instance


router = APIRouter()



@router.get("/getdata/")
async def UserDataAPI(request: Request,background_tasks:BackgroundTasks):
    query = '''
        select au.id,au.first_name,
        CASE WHEN rp.phone IS NOT NULL THEN 1 ELSE 0 END AS has_phone,
        au.date_joined, q2.created_at as first_submission_date,
        (EXTRACT(EPOCH FROM q2.created_at-au.date_joined)/3600) as "delay_hours",
        rp.last_activity
        from residency_profile rp inner join auth_user au on rp.user_id = au.id
        left join
        (select p2t.profile_id, p2t.created_at from residency_profile2task p2t inner join residency_task rt on p2t.task_id = rt.id and rt.project_id is not null
        inner join residency_level lvl on rt.level_id = lvl.id and lvl.level = 1) q2 on q2.profile_id = rp.id
        '''
    response_data = await request.app.state.db.fetch_rows(query)
    data = jsonable_encoder(response_data)
    background_tasks.add_task(tasks._run_task,data)
    return data