import api from './index'

// 获取精灵图鉴（支持 rarity/element/page 筛选）
export const getElves = (params = {}) => {
  return api.get('/elves', { params })
}

export const getElf = (id) => {
  return api.get(`/elves/${id}`)
}

export const getMyElves = () => {
  return api.get('/elves/mine')
}

export const setActiveElf = (id) => {
  return api.post(`/elves/${id}/set-active`)
}
