import { useState } from 'react'
import { submitCode } from '../../api/client'

export default function CodeEditor({ problemId }) {
  const [language, setLanguage] = useState('python')
  const [code, setCode]         = useState('# Write your solution here\n')
  const [result, setResult]     = useState(null)
  const [loading, setLoading]   = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    setResult(null)
    const data = await submitCode(problemId, language, code)
    setResult(data)
    setLoading(false)
  }

  return (
    <div style={{ fontFamily: 'sans-serif' }}>
      <div style={{ marginBottom: 8 }}>
        <select value={language} onChange={e => setLanguage(e.target.value)}
                style={{ padding: '4px 8px' }}>
          <option value="python">Python</option>
          <option value="cpp">C++</option>
          <option value="java">Java</option>
        </select>
      </div>

      <textarea
        value={code}
        onChange={e => setCode(e.target.value)}
        style={{ width: '100%', height: 320, fontFamily: 'monospace',
                 fontSize: 14, padding: 12, boxSizing: 'border-box',
                 border: '1px solid #ccc', borderRadius: 6 }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: 8, padding: '8px 24px', background: '#2563eb',
                 color: 'white', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>

      {result && (
        <div style={{ marginTop: 16, padding: 12, background: '#f0fdf4',
                      border: '1px solid #86efac', borderRadius: 6 }}>
          <b>Submission #{result.submission_id}</b> — {result.verdict}
        </div>
      )}
    </div>
  )
}