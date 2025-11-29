import request from "../request";

const CLUB_NOTICE_LIST = "/notices/public"
const CLUB_ACTIVITIES_LIST = "/activities/public"

export const RequestNoticeList = () => request.get(CLUB_NOTICE_LIST)
export const RequestActivitiesList = () => request.get(CLUB_ACTIVITIES_LIST)