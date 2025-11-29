import request from "../request";

// 加载社团详情
const CLUB_DETAIL_URL = "club/detail/"
const CLUB_CHECK_MEMBERSHIP="members/check?userId="
const CLUB_JOIN_CLUB = "/members/join"
const CLUB_QUIT_CLUB = "/members/quit"

export const RequestClubDetail = (clubId) => request.get(CLUB_DETAIL_URL+clubId)
export const RequestCheckMembership = (userId,clubId) => request.get(CLUB_CHECK_MEMBERSHIP+userId+"&clubId="+clubId)
export const RequestJoinClub = (userId,clubId,remark) => request.post(CLUB_JOIN_CLUB,{
	userId: userId,
	clubId: clubId,
	remark: remark
})
export const RequestQuitClub  = (userId,clubId) => request.post(CLUB_QUIT_CLUB,{
	userId: userId,
	clubId: clubId
})