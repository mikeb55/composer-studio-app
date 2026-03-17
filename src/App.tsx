import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { GenerateView } from './views/GenerateView'
import { HybridGenerateView } from './views/HybridGenerateView/HybridGenerateView'
import { ScorePage } from './pages/ScorePage'
import { ProjectPage } from './pages/ProjectPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <nav className="app-nav">
        <Link to="/">Preset</Link>
        <Link to="/hybrid">Hybrid</Link>
        <Link to="/score">Score</Link>
        <Link to="/projects">Projects</Link>
      </nav>
      <Routes>
        <Route path="/" element={<GenerateView />} />
        <Route path="/hybrid" element={<HybridGenerateView />} />
        <Route path="/score" element={<ScorePage />} />
        <Route path="/projects" element={<ProjectPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
