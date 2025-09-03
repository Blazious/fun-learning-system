import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function DashboardPage() {
	const [me, setMe] = useState(null)
	const [error, setError] = useState('')

	useEffect(() => {
		async function load() {
			try {
				const token = localStorage.getItem('access')
				const res = await axios.get('/api/auth/users/me/', { headers: { Authorization: `Bearer ${token}` } })
				setMe(res.data)
			} catch (_) {
				setError('Failed to load user')
			}
		}
		load()
	}, [])

	function logout() {
		localStorage.removeItem('access')
		localStorage.removeItem('refresh')
		window.location.href = '/login'
	}

	return (
		<div>
			<h1>Dashboard</h1>
			{me ? (
				<div>
					<p>Hello, {me.username} ({me.email})</p>
					<button onClick={logout}>Logout</button>
				</div>
			) : (
				<p>Loading...</p>
			)}
			{error && <div>{error}</div>}
		</div>
	)
}


