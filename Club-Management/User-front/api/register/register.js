import request from "../request";

const CLUB_REGISTER_CLUB = "/register";

export const RequestClubRegister = (username,password,name,deptId,gender)=>request.post(CLUB_REGISTER_CLUB,{
	username: username,
	password: password,
	name: name,
	deptId:deptId,
	gender: gender
})