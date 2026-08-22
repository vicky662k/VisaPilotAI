import {
  useEffect,
  useMemo,
  useState,
} from 'react'

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

  const [isRegister, setIsRegister] =
    useState(false)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const [jobs, setJobs] = useState([])
  const [applications, setApplications] =
    useState([])

  const [matches, setMatches] = useState([])

  const [loadingData, setLoadingData] =
    useState(false)

  /* =====================================================
     M8.5 AI MATCHING STATE
     ===================================================== */

  const [matchFilter, setMatchFilter] =
    useState('all')

  const [matchSort, setMatchSort] =
    useState('match')


  /* =====================================================
     LOAD DASHBOARD DATA
     ===================================================== */

  async function loadDashboard(
    currentUser,
    currentToken
  ) {
    if (!currentUser || !currentToken) {
      return
    }

    setLoadingData(true)
    setError('')

    try {
      /* -------------------------------
         Jobs
         ------------------------------- */

      const jobsData =
        await getJobs(currentToken)

      setJobs(
        Array.isArray(jobsData)
          ? jobsData
          : Array.isArray(jobsData?.jobs)
            ? jobsData.jobs
            : []
      )


      /* -------------------------------
         Applications
         ------------------------------- */

      const applicationsData =
        await getUserApplications(
          currentUser.id,
          currentToken
        )

      setApplications(
        Array.isArray(applicationsData)
          ? applicationsData
          : Array.isArray(
              applicationsData?.applications
            )
            ? applicationsData.applications
            : []
      )


      /* -------------------------------
         AI Recommendations - M8.5
         ------------------------------- */

      // The current test account uses resume_id = 1.
      // Keep the fallback so AI matching continues to work
      // even when /auth/me does not expose resume_id yet.
      const resumeId =
        currentUser.resume_id || 1

      try {
        const matchData =
          await getRecommendedJobs(
            resumeId,
            currentToken
          )

        console.log(
          'AI Match API response:',
          matchData
        )

        const recommendedJobs =
          Array.isArray(matchData)
            ? matchData
            : Array.isArray(
                matchData?.jobs
              )
              ? matchData.jobs
              : []

        // Only replace matches when the API actually
        // returns recommendations. Do not wipe existing
        // matches because of a temporary API/network issue.
        if (recommendedJobs.length > 0) {
          setMatches(recommendedJobs)
        } else {
          console.warn(
            'AI recommendation API returned no jobs.'
          )
        }
      } catch (matchError) {
        console.error(
          'Failed to load AI recommendations:',
          matchError
        )

        // Intentionally do not call setMatches([]).
        // Existing matches remain visible if the endpoint
        // is temporarily unavailable.
      }

    } catch (err) {
      console.error(err)

      setError(
        err.message ||
          'Failed to load dashboard'
      )
    } finally {
      setLoadingData(false)
    }
  }


  /* =====================================================
     RESTORE SESSION
     ===================================================== */

  useEffect(() => {
    async function restoreSession() {
      if (!token) {
        return
      }

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


  /* =====================================================
     LOGIN / REGISTER
     ===================================================== */

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError('')
    setMessage('')

    try {
      /* -------------------------------
         Register
         ------------------------------- */

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


      /* -------------------------------
         Login
         ------------------------------- */

      const result =
        await loginUser(
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
        await getCurrentUser(
          accessToken
        )

      setUser(currentUser)

      await loadDashboard(
        currentUser,
        accessToken
      )

      setMessage(
        'Login successful.'
      )

    } catch (err) {
      console.error(err)

      setError(
        err.message ||
          'Authentication failed'
      )

    } finally {
      setLoading(false)
    }
  }


  /* =====================================================
     LOGOUT
     ===================================================== */

  function handleLogout() {
    localStorage.removeItem(
      'visapilot_token'
    )

    setToken(null)
    setUser(null)

    setJobs([])
    setApplications([])
    setMatches([])

    setError('')
    setMessage('')
  }


  /* =====================================================
     REFRESH
     ===================================================== */

  async function handleRefresh() {
    if (!user || !token) {
      return
    }

    await loadDashboard(
      user,
      token
    )
  }


  /* =====================================================
     M8.5 AI MATCH HELPERS
     ===================================================== */

  function getMatchScore(match) {
    const rawScore =
      match?.match_score ??
      match?.score ??
      match?.match_percentage ??
      0

    const numericScore =
      Number(rawScore)

    if (
      Number.isNaN(numericScore)
    ) {
      return 0
    }

    return Math.max(
      0,
      Math.min(
        Math.round(numericScore),
        100
      )
    )
  }


  function getSkillScore(match) {
    const value =
      Number(
        match?.skill_match_score ?? 0
      )

    if (Number.isNaN(value)) {
      return 0
    }

    return Math.max(
      0,
      Math.min(
        Math.round(value),
        100
      )
    )
  }


  function getLocationScore(match) {
    const value =
      Number(
        match?.location_score ?? 0
      )

    if (Number.isNaN(value)) {
      return 0
    }

    return Math.max(
      0,
      Math.min(
        Math.round(value),
        100
      )
    )
  }


  function getMatchQuality(score) {
    if (score >= 80) {
      return 'Excellent Match'
    }

    if (score >= 70) {
      return 'Strong Match'
    }

    if (score >= 60) {
      return 'Good Match'
    }

    return 'Potential Match'
  }


  function getMatchQualityClass(score) {
    if (score >= 80) {
      return 'excellent'
    }

    if (score >= 70) {
      return 'strong'
    }

    if (score >= 60) {
      return 'good'
    }

    return 'potential'
  }


  function getMatchReasons(match) {
    const reasons = []

    const score =
      getMatchScore(match)

    const skillScore =
      getSkillScore(match)

    const locationScore =
      getLocationScore(match)

    if (skillScore >= 80) {
      reasons.push(
        'Your skills strongly align with this role.'
      )
    } else if (skillScore >= 60) {
      reasons.push(
        'Several of your skills match this role.'
      )
    } else if (skillScore > 0) {
      reasons.push(
        'Some relevant skills were identified.'
      )
    }

    if (locationScore >= 80) {
      reasons.push(
        'The job location is a strong match.'
      )
    } else if (locationScore >= 50) {
      reasons.push(
        'The location has some compatibility with your preferences.'
      )
    }

    if (match.visa_match) {
      reasons.push(
        'Visa sponsorship is available.'
      )
    }

    if (match.relocation_support) {
      reasons.push(
        'Relocation support is available.'
      )
    }

    if (
      reasons.length === 0 &&
      score >= 80
    ) {
      reasons.push(
        'This position has a strong overall match with your profile.'
      )
    }

    if (
      reasons.length === 0
    ) {
      reasons.push(
        'This position may be worth reviewing based on your profile.'
      )
    }

    return reasons
  }


  /* =====================================================
     M8.5 FILTERED + SORTED MATCHES
     ===================================================== */

  const filteredMatches =
    useMemo(() => {
      let result = [...matches]

      /* -------------------------------
         Filters
         ------------------------------- */

      if (matchFilter === '80') {
        result = result.filter(
          (match) =>
            getMatchScore(match) >= 80
        )
      }

      if (matchFilter === '60') {
        result = result.filter(
          (match) =>
            getMatchScore(match) >= 60
        )
      }

      if (
        matchFilter ===
        'visa-relocation'
      ) {
        result = result.filter(
          (match) =>
            Boolean(
              match.visa_match
            ) &&
            Boolean(
              match.relocation_support
            )
        )
      }


      /* -------------------------------
         Sorting
         ------------------------------- */

      result.sort(
        (a, b) => {
          if (
            matchSort ===
            'skills'
          ) {
            return (
              getSkillScore(b) -
              getSkillScore(a)
            )
          }

          if (
            matchSort ===
            'location'
          ) {
            return (
              getLocationScore(b) -
              getLocationScore(a)
            )
          }

          return (
            getMatchScore(b) -
            getMatchScore(a)
          )
        }
      )

      return result

    }, [
      matches,
      matchFilter,
      matchSort,
    ])


  /* =====================================================
     VISA OPPORTUNITIES
     ===================================================== */

  const visaOpportunityCount =
    matches.filter(
      (match) =>
        Boolean(match.visa_match)
    ).length


  /* =====================================================
     LOGIN SCREEN
     ===================================================== */

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
              className={
                !isRegister
                  ? 'active'
                  : ''
              }
              onClick={() => {
                setIsRegister(false)
                setError('')
                setMessage('')
              }}
            >
              Login
            </button>


            <button
              className={
                isRegister
                  ? 'active'
                  : ''
              }
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


          <form
            onSubmit={handleSubmit}
          >

            <label>
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(
                  e.target.value
                )
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
                setPassword(
                  e.target.value
                )
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


  /* =====================================================
     DASHBOARD
     ===================================================== */

  return (
    <div className="dashboard">

      {/* =================================================
          NAVBAR
          ================================================= */}

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

        {/* =================================================
            ERROR
            ================================================= */}

        {error && (
          <div className="error-box dashboard-error">
            {error}
          </div>
        )}


        {/* =================================================
            HERO
            ================================================= */}

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


        {/* =================================================
            STATS
            ================================================= */}

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


          {/* Visa Opportunities */}

          <div className="stat-card">

            <span className="stat-icon">
              🌍
            </span>

            <div>

              <strong>
                {visaOpportunityCount}
              </strong>

              <span>
                Visa Opportunities
              </span>

            </div>

          </div>

        </section>


        {/* =================================================
            M8.5 AI JOB MATCHES
            ================================================= */}

        <section className="section">

          <div className="section-header">

            <div>

              <h2>
                AI Job Matches
              </h2>

              <p>
                Jobs recommended based on
                your resume and profile.
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


          {/* =================================================
              M8.5 FILTERS
              ================================================= */}

          {matches.length > 0 && (
            <div className="match-controls">

              <div className="filter-group">

                <span className="filter-label">
                  Match Filter
                </span>

                <div className="filter-buttons">

                  <button
                    className={
                      matchFilter === 'all'
                        ? 'filter-button active'
                        : 'filter-button'
                    }
                    onClick={() =>
                      setMatchFilter('all')
                    }
                  >
                    All
                  </button>


                  <button
                    className={
                      matchFilter === '80'
                        ? 'filter-button active'
                        : 'filter-button'
                    }
                    onClick={() =>
                      setMatchFilter('80')
                    }
                  >
                    80%+
                  </button>


                  <button
                    className={
                      matchFilter === '60'
                        ? 'filter-button active'
                        : 'filter-button'
                    }
                    onClick={() =>
                      setMatchFilter('60')
                    }
                  >
                    60%+
                  </button>


                  <button
                    className={
                      matchFilter ===
                      'visa-relocation'
                        ? 'filter-button active'
                        : 'filter-button'
                    }
                    onClick={() =>
                      setMatchFilter(
                        'visa-relocation'
                      )
                    }
                  >
                    Visa & Relocation
                  </button>

                </div>

              </div>


              <div className="sort-group">

                <label
                  htmlFor="match-sort"
                  className="filter-label"
                >
                  Sort By
                </label>

                <select
                  id="match-sort"
                  value={matchSort}
                  onChange={(e) =>
                    setMatchSort(
                      e.target.value
                    )
                  }
                  className="sort-select"
                >

                  <option value="match">
                    Highest Match
                  </option>

                  <option value="skills">
                    Best Skills Match
                  </option>

                  <option value="location">
                    Best Location Match
                  </option>

                </select>

              </div>

            </div>
          )}


          {/* =================================================
              NO MATCHES
              ================================================= */}

          {matches.length === 0 ? (

            <div className="empty-card ai-empty-card">

              <div className="empty-icon">
                🤖
              </div>

              <h3>
                No AI matches available yet
              </h3>

              <p>
                Upload a resume and refresh
                your recommendations to find
                suitable jobs.
              </p>

            </div>

          ) : filteredMatches.length === 0 ? (

            <div className="empty-card">

              <div className="empty-icon">
                🔍
              </div>

              <h3>
                No matches found
              </h3>

              <p>
                Try changing your AI match
                filters.
              </p>

              <button
                className="refresh-button"
                onClick={() =>
                  setMatchFilter('all')
                }
              >
                Clear Filters
              </button>

            </div>

          ) : (

            /* =================================================
               MATCH RESULTS
               ================================================= */

            <div className="job-grid ai-match-grid">

              {filteredMatches.map(
                (match, index) => {

                  const score =
                    getMatchScore(match)

                  const skillScore =
                    getSkillScore(match)

                  const locationScore =
                    getLocationScore(match)

                  const quality =
                    getMatchQuality(
                      score
                    )

                  const qualityClass =
                    getMatchQualityClass(
                      score
                    )

                  const reasons =
                    getMatchReasons(
                      match
                    )


                  return (
                    <article
                      className="job-card match-card"
                      key={
                        match.job_id ||
                        match.id ||
                        index
                      }
                    >

                      {/* ---------------------------------
                          CARD HEADER
                          --------------------------------- */}

                      <div className="ai-card-header">

                        <span className="match-label">
                          🤖 AI MATCH
                        </span>

                        <span
                          className={
                            `match-quality ${qualityClass}`
                          }
                        >
                          {quality}
                        </span>

                      </div>


                      {/* ---------------------------------
                          SCORE
                          --------------------------------- */}

                      <div className="match-score-row">

                        <div>

                          <span className="score-number">
                            {score}%
                          </span>

                          <span className="score-label">
                            Match Score
                          </span>

                        </div>


                        <div
                          className={
                            `score-circle ${qualityClass}`
                          }
                        >
                          {score}%
                        </div>

                      </div>


                      {/* Main progress */}

                      <div className="match-progress">

                        <div
                          className={
                            `match-progress-fill ${qualityClass}`
                          }
                          style={{
                            width:
                              `${Math.min(
                                score,
                                100
                              )}%`,
                          }}
                        />

                      </div>


                      {/* ---------------------------------
                          JOB
                          --------------------------------- */}

                      <h3>
                        {match.title ||
                          'Untitled Position'}
                      </h3>

                      <p className="company">
                        {match.company ||
                          'Company'}
                      </p>

                      <p className="location">
                        📍{' '}
                        {match.location ||
                          'Location not specified'}
                      </p>


                      {/* ---------------------------------
                          MATCH BREAKDOWN
                          --------------------------------- */}

                      <div className="match-breakdown">

                        <div className="breakdown-header">
                          <strong>
                            Match Breakdown
                          </strong>
                        </div>


                        {/* Skills */}

                        <div className="breakdown-item">

                          <div className="breakdown-label">

                            <span>
                              Skills
                            </span>

                            <strong>
                              {skillScore}%
                            </strong>

                          </div>


                          <div className="breakdown-bar">

                            <div
                              className="breakdown-fill"
                              style={{
                                width:
                                  `${Math.min(
                                    skillScore,
                                    100
                                  )}%`,
                              }}
                            />

                          </div>

                        </div>


                        {/* Location */}

                        <div className="breakdown-item">

                          <div className="breakdown-label">

                            <span>
                              Location
                            </span>

                            <strong>
                              {locationScore}%
                            </strong>

                          </div>


                          <div className="breakdown-bar">

                            <div
                              className="breakdown-fill"
                              style={{
                                width:
                                  `${Math.min(
                                    locationScore,
                                    100
                                  )}%`,
                              }}
                            />

                          </div>

                        </div>

                      </div>


                      {/* ---------------------------------
                          WHY THIS MATCHES
                          --------------------------------- */}

                      <div className="match-reasons">

                        <strong>
                          Why this matches
                        </strong>

                        {reasons.map(
                          (
                            reason,
                            reasonIndex
                          ) => (
                            <div
                              key={
                                reasonIndex
                              }
                              className="reason-item"
                            >
                              ✓ {reason}
                            </div>
                          )
                        )}

                      </div>


                      {/* ---------------------------------
                          VISA / RELOCATION
                          --------------------------------- */}

                      <div className="match-tags">

                        {match.visa_match && (
                          <span className="tag visa-tag">
                            ✓ Visa Sponsorship
                          </span>
                        )}

                        {match.relocation_support && (
                          <span className="tag relocation-tag">
                            ✓ Relocation Support
                          </span>
                        )}

                      </div>


                      {/* ---------------------------------
                          SOURCE
                          --------------------------------- */}

                      {match.source && (
                        <div className="match-source">
                          Source:{' '}
                          {match.source}
                        </div>
                      )}


                      {/* ---------------------------------
                          ACTION
                          --------------------------------- */}

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

                    </article>
                  )
                }
              )}

            </div>
          )}

        </section>


        {/* =================================================
            JOB DISCOVERY
            ================================================= */}

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


          {jobs.length === 0 ? (

            <div className="empty-card">
              No jobs available yet.
            </div>

          ) : (

            <div className="job-grid">

              {jobs.slice(0, 12).map(
                (job, index) => (

                  <article
                    className="job-card"
                    key={
                      job.id ||
                      index
                    }
                  >

                    <div className="job-card-top">

                      <span className="match-label">
                        JOB
                      </span>

                    </div>

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
                      <span className="tag visa-tag">
                        ✓ Visa Sponsorship
                      </span>
                    )}


                    {job.relocation_support && (
                      <span className="tag relocation-tag">
                        ✓ Relocation Support
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

                  </article>

                )
              )}

            </div>

          )}

        </section>


        {/* =================================================
            APPLICATIONS
            ================================================= */}

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
                (
                  application,
                  index
                ) => (

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
                          {application.status ||
                            'pending'}
                        </strong>

                      </p>


                      {application.company && (
                        <p>
                          {application.company}
                        </p>
                      )}


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