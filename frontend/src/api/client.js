const BASE = "http://localhost:8000"

export const getProblems = () =>
  fetch(`${BASE}/problems`).then(r => r.json())

export const getProblem = (id) =>
  fetch(`${BASE}/problems/${id}`).then(r => r.json())

export const submitCode = (problem_id, language, code) =>
  fetch(`${BASE}/submissions`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ problem_id, language, code })
  }).then(r => r.json())