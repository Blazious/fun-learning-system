import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function MentorshipPage() {
	const [programs, setPrograms] = useState([])
	const [error, setError] = useState('')

	useEffect(() => {
		async function load() {
			try {
				const token = localStorage.getItem('access')
				const res = await axios.get('/api/mentorship/programs/', { headers: { Authorization: `Bearer ${token}` } })
				setPrograms(Array.isArray(res.data) ? res.data : [])
				setError('')
			} catch (e) {
				const msg = e.response?.data?.detail || e.response?.statusText || e.message || 'Failed to load programs'
				setError(msg)
			}
		}
		load()
	}, [])

	return (
		<div>
			<h1>Mentorship Programs</h1>
			{error && <div>{error}</div>}
			{!error && programs.length === 0 && <div>No programs yet.</div>}
			<ul>
				{programs.map((p) => (
					<li key={p.id}>{p.name || p.title}</li>
				))}
			</ul>
		</div>
	)
}


