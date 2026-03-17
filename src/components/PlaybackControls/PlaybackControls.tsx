import { useState } from 'react'
import {
  playbackPlay,
  playbackStop,
  playbackPause,
  playbackLoop,
  type PlaybackStatus,
} from '../../api/client'
import './PlaybackControls.css'

export interface PlaybackControlsProps {
  /** MusicXML string (used when no file path) */
  musicxml?: string | null
  /** Path to MusicXML file (e.g. /outputs/foo.musicxml) */
  filePath?: string | null
  /** Compact mode for inline use */
  compact?: boolean
}

export function PlaybackControls({
  musicxml,
  filePath,
  compact = false,
}: PlaybackControlsProps) {
  const [status, setStatus] = useState<PlaybackStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loopStart, setLoopStart] = useState<number | ''>('')
  const [loopEnd, setLoopEnd] = useState<number | ''>('')

  const hasSource = !!(musicxml || filePath)

  const handlePlay = async () => {
    if (!hasSource) {
      setError('No score to play')
      return
    }
    setLoading(true)
    setError(null)
    try {
      const res = await playbackPlay({
        file_path: filePath || undefined,
        musicxml: musicxml || undefined,
        loop_start: loopStart !== '' ? Number(loopStart) : undefined,
        loop_end: loopEnd !== '' ? Number(loopEnd) : undefined,
      })
      setStatus(res)
      if (res.status === 'playback_not_implemented' || res.status === 'error') {
        setError(res.message || 'Playback not available')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Play failed')
    } finally {
      setLoading(false)
    }
  }

  const handleStop = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await playbackStop()
      setStatus(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Stop failed')
    } finally {
      setLoading(false)
    }
  }

  const handlePause = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await playbackPause()
      setStatus(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Pause failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLoopApply = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await playbackLoop(
        loopStart !== '' ? Number(loopStart) : undefined,
        loopEnd !== '' ? Number(loopEnd) : undefined
      )
      setStatus(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Loop failed')
    } finally {
      setLoading(false)
    }
  }

  const state = status?.state ?? 'stopped'

  return (
    <div className={`playback-controls ${compact ? 'playback-controls-compact' : ''}`}>
      <div className="playback-controls-buttons">
        <button
          type="button"
          className="playback-btn playback-play"
          onClick={handlePlay}
          disabled={!hasSource || loading}
          title="Play"
          aria-label="Play"
        >
          ▶
        </button>
        <button
          type="button"
          className="playback-btn playback-stop"
          onClick={handleStop}
          disabled={loading}
          title="Stop"
          aria-label="Stop"
        >
          ■
        </button>
        <button
          type="button"
          className="playback-btn playback-pause"
          onClick={handlePause}
          disabled={loading}
          title="Pause"
          aria-label="Pause"
        >
          ⏸
        </button>
      </div>

      {!compact && (
        <div className="playback-controls-loop">
          <label>
            Loop
            <input
              type="number"
              min={1}
              placeholder="Start"
              value={loopStart}
              onChange={(e) => setLoopStart(e.target.value === '' ? '' : parseInt(e.target.value, 10))}
            />
          </label>
          <span>–</span>
          <label>
            <input
              type="number"
              min={1}
              placeholder="End"
              value={loopEnd}
              onChange={(e) => setLoopEnd(e.target.value === '' ? '' : parseInt(e.target.value, 10))}
            />
          </label>
          <button
            type="button"
            className="playback-loop-apply"
            onClick={handleLoopApply}
            disabled={loading}
          >
            Set
          </button>
        </div>
      )}

      {status && (
        <span className="playback-status-badge" data-state={state}>
          {state}
        </span>
      )}

      {error && (
        <div className="playback-error" title={error}>
          {error}
        </div>
      )}
    </div>
  )
}

export default PlaybackControls
