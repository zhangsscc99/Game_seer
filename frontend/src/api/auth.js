import api from './index'

export const login = (email, password) => {
  return api.post('/auth/login', { email, password })
}

export const register = (username, email, password) => {
  return api.post('/auth/register', { username, email, password })
}

export const getMe = () => {
  return api.get('/auth/me')
}

export const logout = () => {
  return api.post('/auth/logout')
}
