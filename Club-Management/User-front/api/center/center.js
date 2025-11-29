import request from "../request";

const CLUB_LOADINFO_CLUB = "/user/detail/"

export const RequestUserInfo = (userId) => request.get(CLUB_LOADINFO_CLUB+userId)