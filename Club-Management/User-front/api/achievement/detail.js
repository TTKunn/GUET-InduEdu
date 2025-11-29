import request from "../request";

const CLUB_LOAD_ACHIEVEMENT_DETAIL = "/achievements/detail/"

export const RequstLoadAchievement = (achievementId) => request.get(CLUB_LOAD_ACHIEVEMENT_DETAIL+achievementId)
