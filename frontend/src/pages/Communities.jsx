import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function CommunitiesPage() {
	const [communities, setCommunities] = useState([])
	const [error, setError] = useState('')

	useEffect(() => {
		async function load() {
			try {
				const token = localStorage.getItem('access')
				const res = await axios.get('/api/communities/', { headers: { Authorization: `Bearer ${token}` } })
				setCommunities(res.data)
			} catch (_) {
				setError('Failed to load communities')
			}
		}
		load()
	}, [])

	return (
		<div>
			<h1>Communities</h1>
			{error && <div>{error}</div>}
			<ul>
				{communities.map((c) => (
					<li key={c.id || c.slug}>{c.name}</li>
				))}
			</ul>
		</div>
	)
}


