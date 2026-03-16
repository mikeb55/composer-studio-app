import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { GenerateView } from './views/GenerateView'
import { HybridGenerateView } from './views/HybridGenerateView/HybridGenerateView'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <nav className="app-nav">
        <Link to="/">Preset</Link>
        <Link to="/hybrid">Hybrid</Link>
      </nav>
      <Routes>
        <Route path="/" element={<GenerateView />} />
        <Route path="/hybrid" element={<HybridGenerateView />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
