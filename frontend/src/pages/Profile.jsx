import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function ProfilePage() {
	const [user, setUser] = useState(null)
	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [message, setMessage] = useState('')

	useEffect(() => {
		const token = localStorage.getItem('access')
		axios.get('/api/auth/users/me/', { headers: { Authorization: `Bearer ${token}` } })
			.then(res => {
				setUser(res.data)
				// if your backend uses first_name/last_name on user
				setFirstName(res.data.first_name || '')
				setLastName(res.data.last_name || '')
			})
	}, [])

	async function handleUpdate(e) {
		e.preventDefault()
		setMessage('')
		try {
			const token = localStorage.getItem('access')
			await axios.patch('/api/users/profile/', { first_name: firstName, last_name: lastName }, {
				headers: { Authorization: `Bearer ${token}` }
			})
			setMessage('Profile updated')
		} catch (err) {
			setMessage('Update failed')
		}
	}

	return (
		<div>
			<h1>Profile</h1>
			{user && (
				<form onSubmit={handleUpdate}>
					<div>
						<label>First name</label>
						<input value={firstName} onChange={e => setFirstName(e.target.value)} />
					</div>
					<div>
						<label>Last name</label>
						<input value={lastName} onChange={e => setLastName(e.target.value)} />
					</div>
					<button type="submit">Save</button>
					{message && <div>{message}</div>}
				</form>
			)}
		</div>
	)
}


