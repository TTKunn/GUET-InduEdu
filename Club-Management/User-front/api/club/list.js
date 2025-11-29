import request from "../request";

const CLUB_LOAD_LIST = "/clubs/"

export const RequestLoadClubsList = (userId) => request.get(CLUB_LOAD_LIST+userId)