const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    }
  )

  const data = await response
    .json()
    .catch(() => ({}))

  if (!response.ok) {
    throw new Error(
      data.detail || 'Request failed'
    )
  }

  return data
}

// ===============================
// Authentication
// ===============================

export function registerUser(user) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(user),
  })
}

export function loginUser(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    }),
  })
}

export function getCurrentUser(token) {
  return request('/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

// ===============================
// Jobs
// ===============================

export function getJobs(token) {
  return request('/jobs/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

// ===============================
// Applications
// ===============================

export function getUserApplications(
  userId,
  token
) {
  return request(
    `/applications/user/${userId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
}

// ===============================
// AI Matching
// ===============================

export function getRecommendedJobs(
  resumeId,
  token
) {
  return request(
    `/matches/recommended/${resumeId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )
}