import { useState } from 'react'
import {
  registerUser,
  loginUser,
  getCurrentUser,
} from './api'
import './App.css'

function App() {
  const [mode, setMode] = useState('login')

  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    country: 'India',
  })

  const [user, setUser] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(event) {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    })
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setMessage('')
    setError('')
    setLoading(true)

    try {
      if (mode === 'register') {
        const result = await registerUser(form)

        setMessage(
          result.message ||
            'Registration successful. Please login.'
        )

        setMode('login')

        setForm({
          first_name: '',
          last_name: '',
          email: form.email,
          password: '',
          country: 'India',
        })
      } else {
        const result = await loginUser(
          form.email,
          form.password
        )

        localStorage.setItem(
          'visapilotai_token',
          result.access_token
        )

        const currentUser =
          await getCurrentUser(
            result.access_token
          )

        setUser(currentUser)

        setMessage('Login successful.')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem(
      'visapilotai_token'
    )

    setUser(null)
    setMessage('')
    setError('')
  }

  if (user) {
    return (
      <div className="dashboard">

        <header className="navbar">

          <div className="brand">
            VisaPilotAI
          </div>

          <div className="nav-user">

            <span>
              {user.first_name}{' '}
              {user.last_name}
            </span>

            <button
              onClick={logout}
              className="logout-button"
            >
              Logout
            </button>

          </div>

        </header>

        <main className="dashboard-content">

          <h1>
            Welcome back, {user.first_name} 👋
          </h1>

          <p>
            Your VisaPilotAI dashboard is ready.
          </p>

          <div className="dashboard-placeholder">

            <h2>
              M8 Dashboard
            </h2>

            <p>
              Jobs, AI matches and applications
              will appear here.
            </p>

          </div>

        </main>

      </div>
    )
  }

  return (
    <div className="auth-page">

      <div className="auth-container">

        <div className="brand-section">

          <div className="logo-mark">
            V
          </div>

          <h1>
            VisaPilotAI
          </h1>

          <p>
            Your AI-powered international
            career assistant.
          </p>

          <div className="benefits">

            <div>
              ✓ Discover global opportunities
            </div>

            <div>
              ✓ AI-powered job matching
            </div>

            <div>
              ✓ Automate applications
            </div>

          </div>

        </div>

        <div className="auth-card">

          <div className="tabs">

            <button
              className={
                mode === 'login'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={() => {
                setMode('login')
                setMessage('')
                setError('')
              }}
            >
              Login
            </button>

            <button
              className={
                mode === 'register'
                  ? 'tab active'
                  : 'tab'
              }
              onClick={() => {
                setMode('register')
                setMessage('')
                setError('')
              }}
            >
              Create Account
            </button>

          </div>

          <h2>
            {mode === 'login'
              ? 'Welcome back'
              : 'Create your account'}
          </h2>

          <p className="subtitle">
            {mode === 'login'
              ? 'Sign in to continue to VisaPilotAI.'
              : 'Start your international job search.'}
          </p>

          {message && (
            <div className="success">
              {message}
            </div>
          )}

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>

            {mode === 'register' && (
              <>
                <div className="form-row">

                  <div className="field">

                    <label>
                      First name
                    </label>

                    <input
                      name="first_name"
                      value={
                        form.first_name
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>

                  <div className="field">

                    <label>
                      Last name
                    </label>

                    <input
                      name="last_name"
                      value={
                        form.last_name
                      }
                      onChange={
                        handleChange
                      }
                      required
                    />

                  </div>

                </div>

                <div className="field">

                  <label>
                    Country
                  </label>

                  <input
                    name="country"
                    value={
                      form.country
                    }
                    onChange={
                      handleChange
                    }
                    required
                  />

                </div>
              </>
            )}

            <div className="field">

              <label>
                Email
              </label>

              <input
                type="email"
                name="email"
                value={form.email}
                onChange={
                  handleChange
                }
                placeholder="you@example.com"
                required
              />

            </div>

            <div className="field">

              <label>
                Password
              </label>

              <input
                type="password"
                name="password"
                value={
                  form.password
                }
                onChange={
                  handleChange
                }
                placeholder="Enter your password"
                required
              />

            </div>

            <button
              type="submit"
              className="primary-button"
              disabled={loading}
            >
              {loading
                ? 'Please wait...'
                : mode === 'login'
                  ? 'Sign In'
                  : 'Create Account'}
            </button>

          </form>

          <p className="switch-text">

            {mode === 'login'
              ? "Don't have an account?"
              : 'Already have an account?'}

            <button
              className="link-button"
              onClick={() => {
                setMode(
                  mode === 'login'
                    ? 'register'
                    : 'login'
                )

                setMessage('')
                setError('')
              }}
            >
              {mode === 'login'
                ? ' Create one'
                : ' Sign in'}
            </button>

          </p>

        </div>

      </div>

    </div>
  )
}

export default App