import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Problem from './pages/Problem'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"              element={<Home />} />
        <Route path="/problems/:id"  element={<Problem />} />
      </Routes>
    </BrowserRouter>
  )
}