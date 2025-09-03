import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../lib/api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
	const [user, setUser] = useState(null)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		async function load() {
			const token = localStorage.getItem('access')
			if (!token) { setLoading(false); return }
			try {
				const res = await api.get('/auth/users/me/')
				setUser(res.data)
			} finally {
				setLoading(false)
			}
		}
		load()
	}, [])

	const value = useMemo(() => ({ user, setUser, loading }), [user, loading])
	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() { return useContext(AuthContext) }


