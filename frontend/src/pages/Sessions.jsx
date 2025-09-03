import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function SessionsPage() {
	const [sessions, setSessions] = useState([])
	const [error, setError] = useState('')

	useEffect(() => {
		async function load() {
			try {
				const token = localStorage.getItem('access')
				const res = await axios.get('/api/sessions/', { headers: { Authorization: `Bearer ${token}` } })
				setSessions(res.data)
			} catch (_) {
				setError('Failed to load sessions')
			}
		}
		load()
	}, [])

	return (
		<div>
			<h1>Sessions</h1>
			{error && <div>{error}</div>}
			<ul>
				{sessions.map((s) => (
					<li key={s.id || s.pk}>{s.title || s.name}</li>
				))}
			</ul>
		</div>
	)
}


