import request from "../request";

const CLUB_LOAD_DEPTLIST = "/dept/list"
const CLUB_UPDATE_USER = "/user/update"

export const RequestLoadDeptList = () => request.get(CLUB_LOAD_DEPTLIST)
export const RequestUpdateUser = (formData) => request.post(CLUB_UPDATE_USER,formData)