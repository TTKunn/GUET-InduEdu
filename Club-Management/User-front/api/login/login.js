import request from "../request";

const CLUB_LOGIN_URL = "/login?username=";

export const RequestLoginClub = (username,password) => request.get(CLUB_LOGIN_URL+username+"&password="+password)