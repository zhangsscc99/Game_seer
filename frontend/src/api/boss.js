import api from './index'

export const getBossList = () => {
  return api.get('/boss')
}

export const getBoss = (id) => {
  return api.get(`/boss/${id}`)
}

export const challengeBoss = (id) => {
  return api.post(`/boss/${id}/challenge`)
}
