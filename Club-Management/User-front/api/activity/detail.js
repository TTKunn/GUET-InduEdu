import request from "../request";

const CLUB_ACTIVITY_DETAIL = "/activities/" 
const CLUB_ACTIVITIES_JOIN = "/activities/join"

export const RequestActivityDetail = (id) => request.get(CLUB_ACTIVITY_DETAIL+id)
export const RequestActivitiesJoin = (activityId,userId) => request.post(CLUB_ACTIVITIES_JOIN,{
          activityId: activityId,
          userId: userId
        })