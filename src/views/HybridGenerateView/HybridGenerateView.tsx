import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  listEngines,
  generateHybrid,
  exportMusicXml,
  validateCandidate,
  saveRunToProject,
  type Candidate,
  type EngineRoles,
} from '../../api/client'
import { HybridEngineSelector } from '../../components/HybridEngineSelector'
import { GuardrailStatus } from '../../components/GuardrailStatus'
import { PlaybackControls } from '../../components/PlaybackControls'
import { ScoreViewer } from '../../components/ScoreViewer'
import './HybridGenerateView.css'

export function HybridGenerateView() {
  const navigate = useNavigate()
  const [engines, setEngines] = useState<string[]>([])
  const [roles, setRoles] = useState<EngineRoles>({
    form_engine: 'wayne_shorter',
    harmony_engine: 'wheeler_lyric',
    texture_engine: 'ligeti_texture',
    orchestration_engine: 'big_band',
    counterpoint_engine: '',
  })
  const [inputText, setInputText] = useState('')
  const [count, setCount] = useState(4)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    candidates: Candidate[]
    ranked: Candidate[]
    finalists: Candidate[]
    error?: string
  } | null>(null)
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null)
  const [musicxml, setMusicxml] = useState<string | null>(null)
  const [loadingMusicxml, setLoadingMusicxml] = useState(false)
  const [guardrailStatus, setGuardrailStatus] = useState<'SAFE' | 'WARNING' | 'BLOCKED' | null>(null)
  const [guardrailReasons, setGuardrailReasons] = useState<string[]>([])
  const [exportError, setExportError] = useState<string | null>(null)
  const [saveProjectName, setSaveProjectName] = useState('')
  const [savingToProject, setSavingToProject] = useState(false)
  const [saveProjectError, setSaveProjectError] = useState<string | null>(null)

  useEffect(() => {
    listEngines().then(setEngines).catch(() => setEngines([]))
  }, [])

  const handleGenerate = async () => {
    setLoading(true)
    setResult(null)
    setSelectedCandidate(null)
    setMusicxml(null)
    setGuardrailStatus(null)
    setExportError(null)
    try {
      const res = await generateHybrid({
        engine_roles: roles,
        parameters: {
          input_text: inputText || 'Untitled',
          seed: 0,
          count,
          finalist_count: 5,
        },
      })
      setResult(res)
    } catch (e) {
      setResult({
        candidates: [],
        ranked: [],
        finalists: [],
        error: e instanceof Error ? e.message : 'Generation failed',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSelectCandidate = async (c: Candidate) => {
    setSelectedCandidate(c)
    setMusicxml(null)
    setExportError(null)
    setGuardrailStatus(null)
    setGuardrailReasons([])
    setLoadingMusicxml(true)
    try {
      const validation = await validateCandidate(c)
      setGuardrailStatus(validation.status)
      setGuardrailReasons(validation.reasons || [])

      const { musicxml: xml, error, reasons } = await exportMusicXml(c)
      if (error) {
        setExportError(reasons?.join('; ') || error)
        setMusicxml(null)
      } else {
        setMusicxml(xml)
        setExportError(null)
      }
    } catch {
      setMusicxml(null)
      setExportError('Export failed')
    } finally {
      setLoadingMusicxml(false)
    }
  }

  const handleSaveToProject = async () => {
    const name = saveProjectName.trim()
    if (!name || !musicxml) return
    setSavingToProject(true)
    setSaveProjectError(null)
    try {
      await saveRunToProject({
        project_name: name,
        musicxml,
        engine: roles.harmony_engine || roles.form_engine || 'hybrid',
        input_text: inputText || 'Untitled',
        seed: 0,
        candidates: result?.candidates,
        selected_candidate: selectedCandidate ?? undefined,
      })
      setSaveProjectName('')
    } catch (e) {
      setSaveProjectError(e instanceof Error ? e.message : 'Save failed')
    } finally {
      setSavingToProject(false)
    }
  }

  return (
    <div className="hybrid-generate-view">
      <header className="hybrid-generate-header">
        <h1>Hybrid Engine</h1>
        <p>Combine engines for hybrid compositions</p>
      </header>

      <section className="hybrid-generate-panel">
        <HybridEngineSelector
          engines={engines}
          roles={roles}
          onChange={(r) => setRoles(r)}
        />

        <div className="hybrid-parameters">
          <h3>Parameters</h3>
          <div className="param-row">
            <label htmlFor="hybrid-input">Title</label>
            <input
              id="hybrid-input"
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Untitled"
            />
          </div>
          <div className="param-row">
            <label htmlFor="hybrid-count">Count</label>
            <input
              id="hybrid-count"
              type="number"
              min={1}
              max={12}
              value={count}
              onChange={(e) => setCount(parseInt(e.target.value, 10) || 1)}
            />
          </div>
        </div>

        <button
          type="button"
          className="hybrid-generate-btn"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Generating…' : 'Generate Hybrid'}
        </button>
      </section>

      {result && (
        <section className="hybrid-results">
          {result.error && (
            <div className="result-error">{result.error}</div>
          )}
          {result.candidates.length > 0 && (
            <div className="hybrid-candidates-section">
              <h2>Candidates</h2>
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
            </div>
          )}

          {selectedCandidate && (
            <div className="hybrid-notation-section">
              <div className="hybrid-notation-header">
                <h2>Score</h2>
                {musicxml && (
                  <>
                    <PlaybackControls musicxml={musicxml} compact />
                    <button
                      type="button"
                      className="view-score-btn"
                      onClick={() => navigate('/score', { state: { musicxml } })}
                    >
                      View Score
                    </button>
                    <div className="save-to-project">
                      <input
                        type="text"
                        placeholder="Project name"
                        value={saveProjectName}
                        onChange={(e) => setSaveProjectName(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSaveToProject()}
                      />
                      <button
                        type="button"
                        className="save-project-btn"
                        onClick={handleSaveToProject}
                        disabled={savingToProject || !saveProjectName.trim()}
                      >
                        {savingToProject ? 'Saving…' : 'Save to Project'}
                      </button>
                      {saveProjectError && (
                        <span className="save-project-error">{saveProjectError}</span>
                      )}
                    </div>
                  </>
                )}
                {guardrailStatus && (
                  <GuardrailStatus
                    status={guardrailStatus}
                    reasons={guardrailReasons}
                  />
                )}
              </div>
              {exportError && (
                <div className="export-blocked">
                  Export blocked: {exportError}
                </div>
              )}
              {loadingMusicxml ? (
                <div className="score-loading">Loading…</div>
              ) : musicxml ? (
                <div className="score-viewer-wrap">
                  <ScoreViewer musicxml={musicxml} />
                </div>
              ) : !exportError ? (
                <div className="score-error">Could not load score</div>
              ) : null}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
