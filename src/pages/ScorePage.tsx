import { useSearchParams, useLocation, Link } from 'react-router-dom'
import { useMemo } from 'react'
import { ScoreViewer } from '../components/ScoreViewer'
import { PlaybackControls } from '../components/PlaybackControls'
import './ScorePage.css'

/**
 * ScorePage — Display MusicXML score.
 * Supports:
 * - ?file=url — fetch MusicXML from URL (e.g. /api/outputs/foo.musicxml)
 * - location.state.musicxml — MusicXML string (from View Score in generation)
 */
export function ScorePage() {
  const [searchParams] = useSearchParams()
  const location = useLocation()
  const fileUrl = searchParams.get('file')
  const musicxmlFromState = (location.state as { musicxml?: string } | null)?.musicxml

  const musicxmlUrl = useMemo(() => {
    if (fileUrl) {
      if (fileUrl.startsWith('http') || fileUrl.startsWith('/') || fileUrl.startsWith('data:')) {
        return fileUrl
      }
      return `/api/${fileUrl.replace(/^\//, '')}`
    }
    return undefined
  }, [fileUrl])

  return (
    <div className="score-page">
      <header className="score-page-header">
        <Link to="/" className="score-page-back">
          ← Back to Generate
        </Link>
        <h1>Score</h1>
        {(musicxmlFromState || musicxmlUrl) && (
          <PlaybackControls
            musicxml={musicxmlFromState ?? undefined}
            filePath={fileUrl ?? undefined}
          />
        )}
      </header>
      <div className="score-page-content">
        {musicxmlFromState ? (
          <ScoreViewer musicxml={musicxmlFromState} initialZoom={1} />
        ) : musicxmlUrl ? (
          <ScoreViewer musicxmlUrl={musicxmlUrl} initialZoom={1} />
        ) : (
          <div className="score-page-empty">
            <p>No score to display.</p>
            <p>Generate a composition and click &quot;View Score&quot; to see it here.</p>
            <Link to="/">Go to Generate</Link>
          </div>
        )}
      </div>
    </div>
  )
}

export default ScorePage
