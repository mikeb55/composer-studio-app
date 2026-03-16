import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export interface GenerateRequest {
  preset_name: string
  input_text: string
  seed?: number
}

export interface Candidate {
  compiled?: unknown
  melody_engine?: string
  harmony_engine?: string
  counter_engine?: string | null
  rhythm_engine?: string | null
  base_score?: number
  style_fit_score?: number
  adjusted_score?: number
}

export interface GenerateResponse {
  preset?: string
  input_text?: string
  seed?: number
  candidates?: Candidate[]
  ranked?: Candidate[]
  finalists?: Candidate[]
  error?: string
}

export async function generateCandidates(req: GenerateRequest): Promise<GenerateResponse> {
  const { data } = await api.post<GenerateResponse>('/generate', {
    preset_name: req.preset_name,
    input_text: req.input_text,
    seed: req.seed ?? 0,
  })
  return data
}

export async function exportMusicXml(compiled: Candidate): Promise<{ musicxml: string; filename: string }> {
  const { data } = await api.post<{ musicxml: string; filename: string }>('/export/musicxml', {
    compiled,
    filename: 'composition.musicxml',
  })
  return data
}

export async function listPresets(): Promise<string[]> {
  const { data } = await api.get<string[]>('/engines/presets')
  return Array.isArray(data) ? data : []
}
