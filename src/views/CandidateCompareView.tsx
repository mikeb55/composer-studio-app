import { useState, useEffect } from 'react'
import { exportMusicXml, type Candidate } from '../api/client'
import { ScoreViewer } from '../components/ScoreViewer'
import './CandidateCompareView.css'

export interface CandidateCompareViewProps {
  candidates: Candidate[]
  maxCompare?: number
}

export function CandidateCompareView({ candidates, maxCompare = 3 }: CandidateCompareViewProps) {
  const [musicxmlMap, setMusicxmlMap] = useState<Record<number, string>>({})
  const [loading, setLoading] = useState<Record<number, boolean>>({})

  useEffect(() => {
    const slice = candidates.slice(0, maxCompare)
    setMusicxmlMap({})
    setLoading({})
    slice.forEach((c, i) => {
      setLoading((prev) => ({ ...prev, [i]: true }))
      exportMusicXml(c)
        .then(({ musicxml }) => {
          setMusicxmlMap((prev) => ({ ...prev, [i]: musicxml }))
        })
        .finally(() => {
          setLoading((prev) => ({ ...prev, [i]: false }))
        })
    })
  }, [candidates, maxCompare])

  const toCompare = candidates.slice(0, maxCompare)

  if (toCompare.length === 0) {
    return (
      <div className="candidate-compare-view">
        <p className="empty">No candidates to compare</p>
      </div>
    )
  }

  return (
    <div className="candidate-compare-view">
      <h2>Compare Candidates</h2>
      <div className="compare-grid">
        {toCompare.map((c, i) => (
          <div key={i} className="compare-card">
            <div className="compare-header">
              <span>#{i + 1}</span>
              <span className="engines">
                {c.melody_engine ?? '—'}
                {c.harmony_engine && c.harmony_engine !== c.melody_engine
                  ? ` / ${c.harmony_engine}`
                  : ''}
              </span>
              {typeof c.adjusted_score === 'number' && (
                <span className="score">{c.adjusted_score.toFixed(1)}</span>
              )}
            </div>
            <div className="compare-score">
              {loading[i] ? (
                <div className="loading">Loading…</div>
              ) : musicxmlMap[i] ? (
                <ScoreViewer musicxml={musicxmlMap[i]} />
              ) : (
                <div className="error">—</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
