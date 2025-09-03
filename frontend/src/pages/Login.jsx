import React, { useState } from 'react'
import axios from 'axios'

export default function LoginPage() {
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState('')

	async function handleSubmit(e) {
		e.preventDefault()
		setError('')
		setLoading(true)
		try {
			const res = await axios.post('/api/auth/jwt/create/', { email, password })
			localStorage.setItem('access', res.data.access)
			localStorage.setItem('refresh', res.data.refresh)
			window.location.href = '/'
		} catch (err) {
			setError(err.response?.data?.detail || 'Login failed')
		} finally {
			setLoading(false)
		}
	}

	return (
		<div>
			<h1>Login</h1>
			<form onSubmit={handleSubmit}>
				<div>
					<label>Email</label>
					<input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
				</div>
				<div>
					<label>Password</label>
					<input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
				</div>
				<button disabled={loading} type="submit">{loading ? 'Logging in...' : 'Login'}</button>
				{error && <div>{error}</div>}
			</form>
		</div>
	)
}


