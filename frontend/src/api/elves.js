import api from './index'

export const getElves = (params = {}) => {
  return api.get('/elves/', { params })
}

export const getElf = (id) => {
  return api.get(`/elves/${id}`)
}

export const getMyElves = () => {
  return api.get('/elves/my')
}

export const setActiveElf = (id) => {
  return api.post(`/elves/${id}/set-active`)
}
