import api from './index'

export const getProfile = () => {
  return api.get('/profile')
}

export const getStats = () => {
  return api.get('/profile/stats')
}

export const updateProfile = (data) => {
  return api.put('/profile', data)
}
