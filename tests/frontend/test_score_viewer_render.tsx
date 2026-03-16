import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { ScoreViewer } from '../../src/components/ScoreViewer'

const MINIMAL_MUSICXML = `<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="4.0">
  <work><work-title>Test</work-title></work>
  <part-list>
    <score-part id="P1"><part-name>Part</part-name></score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>4</divisions>
        <key><fifths>0</fifths><mode>major</mode></key>
        <time><beats>4</beats><beat-type>4</beat-type></time>
        <clef><sign>G</sign><line>2</line></clef>
      </attributes>
      <note>
        <pitch><step>C</step><octave>4</octave></pitch>
        <duration>4</duration><type>whole</type>
      </note>
    </measure>
  </part>
</score-partwise>`

const mockToolkit = {
  setOptions: vi.fn(),
  loadData: vi.fn().mockReturnValue(true),
  getPageCount: vi.fn().mockReturnValue(1),
  getLog: vi.fn().mockReturnValue(''),
  redoLayout: vi.fn(),
  renderToSVG: vi.fn().mockReturnValue('<svg xmlns="http://www.w3.org/2000/svg"><g id="notation"/></svg>'),
}

vi.mock('verovio/wasm', () => ({
  default: vi.fn(() => Promise.resolve({})),
}))

vi.mock('verovio/esm', () => ({
  VerovioToolkit: class MockVerovioToolkit {
    constructor() {
      Object.assign(this, mockToolkit)
    }
  },
}))

describe('ScoreViewer', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockToolkit.loadData.mockReturnValue(true)
    mockToolkit.getPageCount.mockReturnValue(1)
    mockToolkit.renderToSVG.mockReturnValue('<svg xmlns="http://www.w3.org/2000/svg"><g id="notation"/></svg>')
  })

  it('loads MusicXML file and renders SVG', async () => {
    render(<ScoreViewer musicxml={MINIMAL_MUSICXML} />)

    await waitFor(
      () => {
        const svg = document.querySelector('.score-viewer-svg svg')
        expect(svg).toBeTruthy()
        expect(svg?.innerHTML).toContain('notation')
      },
      { timeout: 5000 }
    )
  })

  it('shows loading state initially', () => {
    render(<ScoreViewer musicxml={MINIMAL_MUSICXML} />)
    expect(screen.getByText(/loading/i)).toBeInTheDocument()
  })

  it('shows error when MusicXML is empty', async () => {
    render(<ScoreViewer musicxml="" />)
    await waitFor(() => {
      expect(screen.getByText(/no musicxml/i)).toBeInTheDocument()
    })
  })
})
