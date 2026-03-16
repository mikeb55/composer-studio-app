import { useState } from 'react'
import { generateCandidates, listPresets, exportMusicXml, type Candidate } from '../api/client'
import { ScoreViewer } from '../components/ScoreViewer'
import { CandidateCompareView } from './CandidateCompareView'
import './GenerateView.css'

export function GenerateView() {
  const [presets, setPresets] = useState<string[]>([])
  const [preset, setPreset] = useState('shorter_head')
  const [inputText, setInputText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    candidates: Candidate[]
    ranked?: Candidate[]
    finalists?: Candidate[]
    error?: string
  } | null>(null)
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null)
  const [musicxml, setMusicxml] = useState<string | null>(null)
  const [loadingMusicxml, setLoadingMusicxml] = useState(false)
  const [viewMode, setViewMode] = useState<'single' | 'compare'>('single')

  const loadPresets = async () => {
    try {
      const list = await listPresets()
      setPresets(list)
      if (list.length && !list.includes(preset)) setPreset(list[0])
    } catch {
      setPresets(['shorter_head', 'barry_bebop', 'hybrid_counterpoint'])
    }
  }

  const handleGenerate = async () => {
    setLoading(true)
    setResult(null)
    setSelectedCandidate(null)
    setMusicxml(null)
    try {
      const res = await generateCandidates({
        preset_name: preset,
        input_text: inputText || 'Untitled',
        seed: 0,
      })
      if (res.error) {
        setResult({ candidates: [], error: res.error })
      } else {
        setResult({
          candidates: res.candidates ?? [],
          ranked: res.ranked,
          finalists: res.finalists,
        })
      }
    } catch (e) {
      setResult({
        candidates: [],
        error: e instanceof Error ? e.message : 'Generation failed',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSelectCandidate = async (c: Candidate) => {
    setSelectedCandidate(c)
    setMusicxml(null)
    setLoadingMusicxml(true)
    try {
      const { musicxml: xml } = await exportMusicXml(c)
      setMusicxml(xml)
    } catch {
      setMusicxml(null)
    } finally {
      setLoadingMusicxml(false)
    }
  }

  return (
    <div className="generate-view">
      <header className="generate-view-header">
        <h1>Composer Studio</h1>
        <p>Generate compositions with creative engines</p>
      </header>

      <section className="generate-view-form">
        <div className="form-row">
          <label htmlFor="preset">Preset</label>
          <select
            id="preset"
            value={preset}
            onChange={(e) => setPreset(e.target.value)}
            onFocus={loadPresets}
          >
            {presets.length ? (
              presets.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))
            ) : (
              <>
                <option value="shorter_head">shorter_head</option>
                <option value="barry_bebop">barry_bebop</option>
                <option value="hybrid_counterpoint">hybrid_counterpoint</option>
              </>
            )}
          </select>
        </div>
        <div className="form-row">
          <label htmlFor="input">Title / Premise</label>
          <input
            id="input"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter composition title or premise"
          />
        </div>
        <button
          type="button"
          className="generate-btn"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Generating…' : 'Generate'}
        </button>
      </section>

      {result && (
        <section className="generate-view-results">
          {result.error && (
            <div className="result-error">{result.error}</div>
          )}
          {result.candidates.length > 0 && (
            <div className="candidates-section">
              <div className="candidates-header">
                <h2>Candidates</h2>
                <div className="view-toggle">
                  <button
                    type="button"
                    className={viewMode === 'single' ? 'active' : ''}
                    onClick={() => setViewMode('single')}
                  >
                    Single
                  </button>
                  <button
                    type="button"
                    className={viewMode === 'compare' ? 'active' : ''}
                    onClick={() => setViewMode('compare')}
                  >
                    Compare
                  </button>
                </div>
              </div>
              {viewMode === 'compare' ? (
                <CandidateCompareView
                  candidates={result.ranked ?? result.finalists ?? result.candidates}
                  maxCompare={3}
                />
              ) : (
              <div className="candidates-list">
                {(result.ranked ?? result.finalists ?? result.candidates).map((c, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`candidate-card ${selectedCandidate === c ? 'selected' : ''}`}
                    onClick={() => handleSelectCandidate(c)}
                  >
                    <span className="candidate-rank">#{i + 1}</span>
                    <span className="candidate-engines">
                      {c.melody_engine ?? '—'}
                      {c.harmony_engine && c.harmony_engine !== c.melody_engine
                        ? ` / ${c.harmony_engine}`
                        : ''}
                    </span>
                    {typeof c.adjusted_score === 'number' && (
                      <span className="candidate-score">{c.adjusted_score.toFixed(1)}</span>
                    )}
                  </button>
                ))}
              </div>
              )}
            </div>
          )}

          {selectedCandidate && (
            <div className="notation-section">
              <h2>Score</h2>
              {loadingMusicxml ? (
                <div className="score-loading">Loading…</div>
              ) : musicxml ? (
                <div className="score-viewer-wrap">
                  <ScoreViewer musicxml={musicxml} />
                </div>
              ) : (
                <div className="score-error">Could not load score</div>
              )}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
