import request from "../request";

const CLUB_ACTIVITIES_PARTICIPATED = "/activities/participated?userId="

export const RequestClubParticipated = (userId,page,pageSize) => request.get(CLUB_ACTIVITIES_PARTICIPATED+userId+"&page="+page+"&pageSize="+pageSize)