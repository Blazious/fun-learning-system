import React from 'react'
import { Routes, Route, Navigate, Link } from 'react-router-dom'
import LoginPage from './pages/Login.jsx'
import RegisterPage from './pages/Register.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import DashboardPage from './pages/Dashboard.jsx'
import ProfilePage from './pages/Profile.jsx'
import SessionsPage from './pages/Sessions.jsx'
import CommunitiesPage from './pages/Communities.jsx'
import MentorshipPage from './pages/Mentorship.jsx'

export default function App() {
	return (
		<AuthProvider>
			<div>
				<nav>
					<Link to="/">Dashboard</Link> | 
					<Link to="/profile">Profile</Link> | 
					<Link to="/sessions">Sessions</Link> | 
					<Link to="/communities">Communities</Link> | 
					<Link to="/mentorship">Mentorship</Link> | 
					<Link to="/login">Login</Link> | 
					<Link to="/register">Register</Link> | 
					<button onClick={() => { localStorage.removeItem('access'); localStorage.removeItem('refresh'); window.location.href = '/login' }}>Logout</button>
				</nav>
				<Routes>
					<Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
					<Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
					<Route path="/sessions" element={<ProtectedRoute><SessionsPage /></ProtectedRoute>} />
					<Route path="/communities" element={<ProtectedRoute><CommunitiesPage /></ProtectedRoute>} />
					<Route path="/mentorship" element={<ProtectedRoute><MentorshipPage /></ProtectedRoute>} />
					<Route path="/login" element={<LoginPage />} />
					<Route path="/register" element={<RegisterPage />} />
					<Route path="*" element={<Navigate to="/" replace />} />
				</Routes>
			</div>
		</AuthProvider>
	)
}


