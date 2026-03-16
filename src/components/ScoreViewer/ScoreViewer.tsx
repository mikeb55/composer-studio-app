import { useEffect, useRef, useState, useCallback } from 'react'
import createVerovioModule from 'verovio/wasm'
import { VerovioToolkit } from 'verovio/esm'
import './ScoreViewer.css'

export type ViewMode = 'scroll' | 'page'

export interface ScoreViewerProps {
  /** MusicXML string content */
  musicxml?: string
  /** URL to fetch MusicXML (used when musicxml string not provided) */
  musicxml_path?: string
  /** Initial zoom level (1 = 100%) */
  initialZoom?: number
  /** View mode: scroll (continuous) or page */
  viewMode?: ViewMode
  /** Callback when score loads */
  onLoad?: () => void
  /** Callback on error */
  onError?: (err: string) => void
}

export function ScoreViewer({
  musicxml,
  musicxml_path,
  initialZoom = 1,
  viewMode = 'page',
  onLoad,
  onError,
}: ScoreViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [toolkit, setToolkit] = useState<VerovioToolkit | null>(null)
  const [svgContent, setSvgContent] = useState<string>('')
  const [pageCount, setPageCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [zoom, setZoom] = useState(initialZoom)
  const [mode, setMode] = useState<ViewMode>(viewMode)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const toolkitRef = useRef<VerovioToolkit | null>(null)

  const loadMusicXml = useCallback(async (xml: string) => {
    if (!xml?.trim()) {
      setError('No MusicXML content')
      setLoading(false)
      return
    }
    try {
      const VerovioModule = await createVerovioModule()
      const vrv = new VerovioToolkit(VerovioModule)
      toolkitRef.current = vrv

      vrv.setOptions(JSON.stringify({
        scale: Math.round(zoom * 50),
        pageWidth: 1200,
        pageHeight: 1600,
      }))

      const ok = vrv.loadData(xml)
      if (!ok) {
        const log = vrv.getLog()
        throw new Error(log || 'Failed to load MusicXML')
      }

      const pages = vrv.getPageCount()
      setPageCount(pages)
      setToolkit(vrv)
      setError(null)
      onLoad?.()
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e)
      setError(msg)
      onError?.(msg)
    } finally {
      setLoading(false)
    }
  }, [zoom, onLoad, onError])

  useEffect(() => {
    if (musicxml_path) {
      setLoading(true)
      fetch(musicxml_path)
        .then((r) => r.text())
        .then(loadMusicXml)
        .catch((e) => {
          setError(e instanceof Error ? e.message : String(e))
          setLoading(false)
        })
    } else if (musicxml !== undefined) {
      setLoading(true)
      loadMusicXml(musicxml)
    } else {
      setLoading(false)
      setSvgContent('')
      setPageCount(0)
    }
  }, [musicxml, musicxml_path, loadMusicXml])

  useEffect(() => {
    if (!toolkit || pageCount === 0) return
    const vrv = toolkit
    vrv.setOptions(JSON.stringify({
      scale: Math.round(zoom * 50),
      pageWidth: 1200,
      pageHeight: 1600,
    }))
    vrv.redoLayout('')
    const svg = vrv.renderToSVG(currentPage, 0)
    setSvgContent(svg)
  }, [toolkit, currentPage, zoom, pageCount])

  const zoomIn = () => setZoom((z) => Math.min(z + 0.25, 3))
  const zoomOut = () => setZoom((z) => Math.max(z - 0.25, 0.5))
  const prevPage = () => setCurrentPage((p) => Math.max(1, p - 1))
  const nextPage = () => setCurrentPage((p) => Math.min(pageCount, p + 1))

  return (
    <div className="score-viewer" ref={containerRef}>
      <div className="score-viewer-toolbar">
        <div className="score-viewer-zoom">
          <button type="button" onClick={zoomOut} aria-label="Zoom out">−</button>
          <span>{Math.round(zoom * 100)}%</span>
          <button type="button" onClick={zoomIn} aria-label="Zoom in">+</button>
        </div>
        <div className="score-viewer-mode">
          <button
            type="button"
            className={mode === 'scroll' ? 'active' : ''}
            onClick={() => setMode('scroll')}
          >
            Scroll
          </button>
          <button
            type="button"
            className={mode === 'page' ? 'active' : ''}
            onClick={() => setMode('page')}
          >
            Page
          </button>
        </div>
        {pageCount > 1 && mode === 'page' && (
          <div className="score-viewer-pages">
            <button type="button" onClick={prevPage} disabled={currentPage <= 1}>‹</button>
            <span>{currentPage} / {pageCount}</span>
            <button type="button" onClick={nextPage} disabled={currentPage >= pageCount}>›</button>
          </div>
        )}
        <div className="score-viewer-playback">
          <button type="button" disabled aria-label="Play">▶ Play</button>
          <button type="button" disabled aria-label="Stop">■ Stop</button>
          <button type="button" disabled aria-label="Loop">↻ Loop</button>
        </div>
      </div>
      <div className={`score-viewer-content score-viewer-${mode}`}>
        {loading && <div className="score-viewer-loading">Loading score…</div>}
        {error && <div className="score-viewer-error">{error}</div>}
        {!loading && !error && svgContent && (
          <div
            className="score-viewer-svg"
            style={{ transform: `scale(${zoom})`, transformOrigin: 'top left' }}
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
        )}
      </div>
    </div>
  )
}

export default ScoreViewer
