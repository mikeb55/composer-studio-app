import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { GenerateView } from './views/GenerateView'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GenerateView />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
