import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getProblem } from '../api/client'
import CodeEditor from '../components/CodeEditor/CodeEditor'

export default function Problem() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [problem, setProblem] = useState(null)

  useEffect(() => { getProblem(id).then(setProblem) }, [id])

  if (!problem) return <p style={{ padding: 32 }}>Loading...</p>

  return (
    <div style={{ display: 'flex', gap: 24, padding: 32, fontFamily: 'sans-serif' }}>

      {/* LEFT — problem info */}
      <div style={{ flex: 1 }}>
        <button onClick={() => navigate('/')} style={{ marginBottom: 16 }}>
          ← Back
        </button>
        <h2>{problem.title}</h2>
        <p><b>Difficulty:</b> {problem.difficulty}</p>
        <p style={{ whiteSpace: 'pre-wrap' }}>{problem.statement}</p>

        <h4>Sample Test Cases</h4>
        {problem.test_cases.map((tc, i) => (
          <div key={i} style={{ background: '#f5f5f5', padding: 12,
                                marginBottom: 8, borderRadius: 6 }}>
            <div><b>Input:</b><br /><code>{tc.input}</code></div>
            <div style={{ marginTop: 6 }}>
              <b>Expected Output:</b><br /><code>{tc.expected_output}</code>
            </div>
          </div>
        ))}
      </div>

      {/* RIGHT — code editor */}
      <div style={{ flex: 1 }}>
        <CodeEditor problemId={parseInt(id)} />
      </div>

    </div>
  )
}