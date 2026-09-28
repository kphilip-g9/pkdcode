import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getProblems } from '../api/client'

export default function Home() {
  const [problems, setProblems] = useState([])
  const navigate = useNavigate()

  useEffect(() => { getProblems().then(setProblems) }, [])

  return (
    <div style={{ padding: 32, fontFamily: 'sans-serif' }}>
      <h1>NexusCP</h1>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={th}>#</th>
            <th style={th}>Title</th>
            <th style={th}>Difficulty</th>
          </tr>
        </thead>
        <tbody>
          {problems.map(p => (
            <tr key={p.id}
                onClick={() => navigate(`/problems/${p.id}`)}
                style={{ cursor: 'pointer' }}>
              <td style={td}>{p.id}</td>
              <td style={td}>{p.title}</td>
              <td style={td}>{p.difficulty}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

const th = { textAlign: 'left', padding: '8px 16px', borderBottom: '2px solid #ccc' }
const td = { padding: '8px 16px', borderBottom: '1px solid #eee' }