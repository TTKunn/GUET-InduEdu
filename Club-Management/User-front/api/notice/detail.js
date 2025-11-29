import request from "../request";

const CLUB_GET_NOTICE = "/notices/"

export const RequestGetNotice = (id) => request.get(CLUB_GET_NOTICE+id)