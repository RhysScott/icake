import request from "@/api/request";

export const login = data => request.post('/user/login', data)

export const logout = data => request.post('/user/logout', data)

export const register = data => request.post('/user/register', data)

export const reset_password = data => request.post('/user/reset-password', data)

export const update_user_info = data => request.post('/user/update', data)

export const get_user_info = () => request.get('/user/info')
