import { useState, useEffect } from 'react'
import { exportMusicXml, type Candidate } from '../api/client'
import { ScoreViewer } from '../components/ScoreViewer'
import './NotationView.css'

export interface NotationViewProps {
  /** Selected candidate to display */
  candidate: Candidate | null
  /** Optional title */
  title?: string
}

export function NotationView({ candidate, title }: NotationViewProps) {
  const [musicxml, setMusicxml] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!candidate) {
      setMusicxml(null)
      setError(null)
      return
    }
    setLoading(true)
    setError(null)
    exportMusicXml(candidate)
      .then(({ musicxml: xml }) => {
        setMusicxml(xml)
      })
      .catch((e) => {
        setError(e instanceof Error ? e.message : 'Failed to load score')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [candidate])

  if (!candidate) {
    return (
      <div className="notation-view">
        <p className="empty">Select a candidate to view notation</p>
      </div>
    )
  }

  return (
    <div className="notation-view">
      <header className="notation-view-header">
        {title && <h2>{title}</h2>}
        <div className="notation-meta">
          <span>{candidate.melody_engine ?? '—'}</span>
          {candidate.harmony_engine && candidate.harmony_engine !== candidate.melody_engine && (
            <span> / {candidate.harmony_engine}</span>
          )}
          {typeof candidate.adjusted_score === 'number' && (
            <span className="score">Score: {candidate.adjusted_score.toFixed(1)}</span>
          )}
        </div>
      </header>
      <div className="notation-viewer">
        {loading && <div className="loading">Loading score…</div>}
        {error && <div className="error">{error}</div>}
        {!loading && !error && musicxml && (
          <ScoreViewer musicxml={musicxml} />
        )}
      </div>
    </div>
  )
}
