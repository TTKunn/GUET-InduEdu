import request from "../request";

const  CLUB_CATEGORY_LIST = "/category/list"
const CLUB_LIST = "/club/list"

export const RequestClubCateGoryList = () => request.get(CLUB_CATEGORY_LIST)
export const RequestClubList = () => request.get(CLUB_LIST)