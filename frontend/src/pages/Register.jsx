import React, { useState } from 'react'
import axios from 'axios'

export default function RegisterPage() {
	const [username, setUsername] = useState('')
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [passwordRetype, setPasswordRetype] = useState('')
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState('')
	const [success, setSuccess] = useState('')

	async function handleSubmit(e) {
		e.preventDefault()
		setError('')
		setSuccess('')
		setLoading(true)
		try {
			await axios.post('/api/users/register/', {
				username,
				email,
				password,
				password_retype: passwordRetype
			})
			setSuccess('Account created. You can now login.')
		} catch (err) {
			const msg = err.response?.data || err.message || 'Registration failed'
			setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
		} finally {
			setLoading(false)
		}
	}

	return (
		<div>
			<h1>Register</h1>
			<form onSubmit={handleSubmit}>
				<div>
					<label>Username</label>
					<input type="text" value={username} onChange={e => setUsername(e.target.value)} required />
				</div>
				<div>
					<label>Email</label>
					<input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
				</div>
				<div>
					<label>Password</label>
					<input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
				</div>
				<div>
					<label>Retype Password</label>
					<input type="password" value={passwordRetype} onChange={e => setPasswordRetype(e.target.value)} required />
				</div>
				<button disabled={loading} type="submit">{loading ? 'Creating...' : 'Create account'}</button>
				{error && <div>{error}</div>}
				{success && <div>{success}</div>}
			</form>
		</div>
	)
}


