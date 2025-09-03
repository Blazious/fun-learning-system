import axios from 'axios'

export const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
	const token = localStorage.getItem('access')
	if (token) config.headers.Authorization = `Bearer ${token}`
	return config
})

api.interceptors.response.use(
	(res) => res,
	async (error) => {
		const original = error.config
		if (error.response?.status === 401 && !original._retry) {
			original._retry = true
			const refresh = localStorage.getItem('refresh')
			if (refresh) {
				try {
					const r = await axios.post('/api/auth/jwt/refresh/', { refresh })
					localStorage.setItem('access', r.data.access)
					original.headers.Authorization = `Bearer ${r.data.access}`
					return api(original)
				} catch (_) {
					localStorage.removeItem('access')
					localStorage.removeItem('refresh')
					window.location.href = '/login'
				}
			}
		}
		return Promise.reject(error)
	}
)


