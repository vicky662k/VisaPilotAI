import { useEffect, useState } from 'react'
import {
  loginUser,
  registerUser,
  getCurrentUser,
  getJobs,
  getUserApplications,
  getRecommendedJobs,
} from './api'
import './App.css'

function App() {
  const [token, setToken] = useState(
    localStorage.getItem('visapilot_token')
  )

  const [user, setUser] = useState(null)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [isRegister, setIsRegister] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [matches, setMatches] = useState([])

  const [loadingData, setLoadingData] = useState(false)

  // --------------------------------
  // Load dashboard data
  // --------------------------------

  async function loadDashboard(currentUser, currentToken) {
    if (!currentUser || !currentToken) return

    setLoadingData(true)
    setError('')

    try {
      // --------------------------------
      // Jobs
      // --------------------------------

      const jobsData = await getJobs(currentToken)

      setJobs(
        Array.isArray(jobsData)
          ? jobsData
          : Array.isArray(jobsData?.jobs)
            ? jobsData.jobs
            : []
      )

      // --------------------------------
      // Applications
      // --------------------------------

      const applicationsData = await getUserApplications(
        currentUser.id,
        currentToken
      )

      setApplications(
        Array.isArray(applicationsData)
          ? applicationsData
          : Array.isArray(applicationsData?.applications)
            ? applicationsData.applications
            : []
      )

      // --------------------------------
      // AI Recommendations - M8.3
      // --------------------------------

      // Use the user's resume_id when available.
      // Current test account uses resume_id = 1.
      const resumeId = currentUser.resume_id || 1

      try {
        const matchData = await getRecommendedJobs(
          resumeId,
          currentToken
        )

        console.log(
          'AI Match API response:',
          matchData
        )

        const recommendedJobs = Array.isArray(matchData)
          ? matchData
          : Array.isArray(matchData?.jobs)
            ? matchData.jobs
            : []

        setMatches(recommendedJobs)
      } catch (matchError) {
        console.error(
          'Failed to load AI recommendations:',
          matchError
        )

        setMatches([])
      }
    } catch (err) {
      console.error(err)

      setError(
        err.message || 'Failed to load dashboard'
      )
    } finally {
      setLoadingData(false)
    }
  }

  // --------------------------------
  // Restore logged-in session
  // --------------------------------

  useEffect(() => {
    async function restoreSession() {
      if (!token) return

      try {
        const currentUser =
          await getCurrentUser(token)

        setUser(currentUser)

        await loadDashboard(
          currentUser,
          token
        )
      } catch (err) {
        console.error(err)

        localStorage.removeItem(
          'visapilot_token'
        )

        setToken(null)
        setUser(null)
      }
    }

    restoreSession()
  }, [])

  // --------------------------------
  // Login / Register
  // --------------------------------

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError('')
    setMessage('')

    try {
      // --------------------------------
      // Register
      // --------------------------------

      if (isRegister) {
        await registerUser({
          email,
          password,
        })

        setMessage(
          'Account created successfully. Please sign in.'
        )

        setIsRegister(false)
        setPassword('')

        return
      }

      // --------------------------------
      // Login
      // --------------------------------

      const result = await loginUser(
        email,
        password
      )

      const accessToken =
        result.access_token ||
        result.token

      if (!accessToken) {
        throw new Error(
          'Login succeeded but no access token was returned.'
        )
      }

      localStorage.setItem(
        'visapilot_token',
        accessToken
      )

      setToken(accessToken)

      const currentUser =
        await getCurrentUser(accessToken)

      setUser(currentUser)

      await loadDashboard(
        currentUser,
        accessToken
      )

      setMessage('Login successful.')
    } catch (err) {
      console.error(err)

      setError(
        err.message || 'Authentication failed'
      )
    } finally {
      setLoading(false)
    }
  }

  // --------------------------------
  // Logout
  // --------------------------------

  function handleLogout() {
    localStorage.removeItem(
      'visapilot_token'
    )

    setToken(null)
    setUser(null)
    setJobs([])
    setApplications([])
    setMatches([])
  }

  // --------------------------------
  // Refresh
  // --------------------------------

  async function handleRefresh() {
    if (!user || !token) return

    await loadDashboard(
      user,
      token
    )
  }

  // --------------------------------
  // Login screen
  // --------------------------------

  if (!token || !user) {
    return (
      <div className="auth-page">

        <div className="auth-brand">

          <div className="brand-icon">
            V
          </div>

          <h1>
            VisaPilotAI
          </h1>

          <p>
            Your AI-powered international
            career assistant.
          </p>

          <div className="features">

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

          <div className="auth-tabs">

            <button
              className={!isRegister ? 'active' : ''}
              onClick={() => {
                setIsRegister(false)
                setError('')
                setMessage('')
              }}
            >
              Login
            </button>

            <button
              className={isRegister ? 'active' : ''}
              onClick={() => {
                setIsRegister(true)
                setError('')
                setMessage('')
              }}
            >
              Create Account
            </button>

          </div>

          <h2>
            {isRegister
              ? 'Create your account'
              : 'Welcome back'}
          </h2>

          <p className="auth-subtitle">
            {isRegister
              ? 'Start your international career journey.'
              : 'Sign in to continue to VisaPilotAI.'}
          </p>

          {error && (
            <div className="error-box">
              {error}
            </div>
          )}

          {message && (
            <div className="success-box">
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit}>

            <label>
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              placeholder="you@example.com"
              required
            />

            <label>
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              placeholder="Enter your password"
              required
            />

            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading
                ? 'Please wait...'
                : isRegister
                  ? 'Create Account'
                  : 'Sign In'}
            </button>

          </form>

          {!isRegister && (
            <p className="switch-text">

              Don't have an account?{' '}

              <button
                onClick={() => {
                  setIsRegister(true)
                  setError('')
                  setMessage('')
                }}
              >
                Create one
              </button>

            </p>
          )}

        </div>

      </div>
    )
  }

  // --------------------------------
  // Dashboard
  // --------------------------------

  return (
    <div className="dashboard">

      {/* Navbar */}

      <header className="navbar">

        <div className="navbar-brand">

          <div className="small-icon">
            V
          </div>

          <span>
            VisaPilotAI
          </span>

        </div>

        <div className="navbar-user">

          <span>
            {user.name ||
              user.full_name ||
              user.email ||
              'User'}
          </span>

          <button
            onClick={handleLogout}
            className="logout-button"
          >
            Logout
          </button>

        </div>

      </header>

      <main className="dashboard-content">

        {/* Error */}

        {error && (
          <div className="error-box dashboard-error">
            {error}
          </div>
        )}

        {/* Hero */}

        <section className="hero">

          <div>

            <div className="eyebrow">
              VISA PILOT AI
            </div>

            <h1>
              Welcome back,{' '}
              {user.name ||
                user.full_name ||
                'there'} 👋
            </h1>

            <p>
              Discover opportunities and
              manage your international
              career applications.
            </p>

          </div>

        </section>

        {/* Stats */}

        <section className="stats-grid">

          {/* Jobs */}

          <div className="stat-card">

            <span className="stat-icon">
              🔎
            </span>

            <div>

              <strong>
                {jobs.length}
              </strong>

              <span>
                Jobs Available
              </span>

            </div>

          </div>

          {/* AI Matches */}

          <div className="stat-card">

            <span className="stat-icon">
              🤖
            </span>

            <div>

              <strong>
                {matches.length}
              </strong>

              <span>
                AI Matches
              </span>

            </div>

          </div>

          {/* Applications */}

          <div className="stat-card">

            <span className="stat-icon">
              📋
            </span>

            <div>

              <strong>
                {applications.length}
              </strong>

              <span>
                Applications
              </span>

            </div>

          </div>

          {/* Interviews */}

          <div className="stat-card">

            <span className="stat-icon">
              🎯
            </span>

            <div>

              <strong>
                {
                  applications.filter(
                    (app) =>
                      app.status ===
                      'interview'
                  ).length
                }
              </strong>

              <span>
                Interviews
              </span>

            </div>

          </div>

        </section>

        {/* =================================
            AI JOB MATCHES - M8.3
           ================================= */}

        <section className="section">

          <div className="section-header">

            <div>

              <h2>
                AI Job Matches
              </h2>

              <p>
                Jobs recommended based on
                your resume.
              </p>

            </div>

            <button
              className="refresh-button"
              onClick={handleRefresh}
              disabled={loadingData}
            >
              {loadingData
                ? 'Refreshing...'
                : 'Refresh'}
            </button>

          </div>

          {matches.length === 0 ? (

            <div className="empty-card">
              No AI matches available yet.
            </div>

          ) : (

            <div className="job-grid">

              {matches.map(
                (match, index) => {

                  const score =
                    match.match_score ??
                    match.score ??
                    match.match_percentage

                  return (

                    <div
                      className="job-card match-card"
                      key={
                        match.job_id ||
                        match.id ||
                        index
                      }
                    >

                      {/* Match Header */}

                      <div className="job-card-top">

                        <span className="match-label">
                          🤖 AI MATCH
                        </span>

                        {score !== undefined && (
                          <span className="score">
                            {score}%
                          </span>
                        )}

                      </div>

                      {/* Job Title */}

                      <h3>
                        {match.title ||
                          'Untitled Position'}
                      </h3>

                      {/* Company */}

                      <p className="company">
                        {match.company ||
                          'Company'}
                      </p>

                      {/* Location */}

                      <p className="location">
                        📍{' '}
                        {match.location ||
                          'Location not specified'}
                      </p>

                      {/* Skill Match */}

                      {match.skill_match_score !==
                        undefined && (

                        <div className="match-detail">

                          <strong>
                            Skills:
                          </strong>{' '}

                          {match.skill_match_score}%

                        </div>

                      )}

                      {/* Visa Sponsorship */}

                      {match.visa_match && (

                        <span className="tag">
                          ✓ Visa Sponsorship
                        </span>

                      )}

                      {/* Relocation Support */}

                      {match.relocation_support && (

                        <span className="tag">
                          ✓ Relocation Support
                        </span>

                      )}

                      {/* Source */}

                      {match.source && (

                        <div className="match-source">
                          Source: {match.source}
                        </div>

                      )}

                      {/* View Job */}

                      <a
                        href={
                          match.job_url ||
                          match.application_url ||
                          match.url ||
                          '#'
                        }
                        target="_blank"
                        rel="noreferrer"
                        className="view-job"
                      >
                        View Job →
                      </a>

                    </div>

                  )
                }
              )}

            </div>

          )}

        </section>

        {/* =================================
            ALL JOBS
           ================================= */}

        <section className="section">

          <div className="section-header">

            <div>

              <h2>
                Job Discovery
              </h2>

              <p>
                Opportunities currently
                available in VisaPilotAI.
              </p>

            </div>

          </div>

          <div className="job-grid">

            {jobs.slice(0, 12).map(
              (job, index) => (

                <div
                  className="job-card"
                  key={
                    job.id ||
                    index
                  }
                >

                  <h3>
                    {job.title ||
                      'Untitled Position'}
                  </h3>

                  <p className="company">
                    {job.company ||
                      job.company_name ||
                      'Company'}
                  </p>

                  <p className="location">
                    📍{' '}
                    {job.location ||
                      'Location not specified'}
                  </p>

                  {job.visa_sponsorship && (

                    <span className="tag">
                      ✓ Visa Sponsorship
                    </span>

                  )}

                  <a
                    href={
                      job.application_url ||
                      job.url ||
                      job.job_url ||
                      '#'
                    }
                    target="_blank"
                    rel="noreferrer"
                    className="view-job"
                  >
                    View Job →
                  </a>

                </div>

              )
            )}

          </div>

        </section>

        {/* =================================
            APPLICATIONS
           ================================= */}

        <section className="section">

          <div className="section-header">

            <div>

              <h2>
                My Applications
              </h2>

              <p>
                Track your job applications.
              </p>

            </div>

          </div>

          {applications.length === 0 ? (

            <div className="empty-card">
              No applications yet.
            </div>

          ) : (

            <div className="application-list">

              {applications.map(
                (application, index) => (

                  <div
                    className="application-card"
                    key={
                      application.id ||
                      index
                    }
                  >

                    <div>

                      <h3>
                        {application.job
                          ?.title ||
                          application.job_title ||
                          `Application #${
                            application.id
                          }`}
                      </h3>

                      <p>
                        Status:{' '}

                        <strong>
                          {application.status}
                        </strong>

                      </p>

                      {application.created_at && (

                        <small>

                          Applied:{' '}

                          {new Date(
                            application.created_at
                          ).toLocaleDateString()}

                        </small>

                      )}

                    </div>

                    {application.application_url && (

                      <a
                        href={
                          application.application_url
                        }
                        target="_blank"
                        rel="noreferrer"
                        className="view-job"
                      >
                        View Application →
                      </a>

                    )}

                  </div>

                )
              )}

            </div>

          )}

        </section>

      </main>

    </div>
  )
}

export default App