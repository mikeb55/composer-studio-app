import axios from 'axios'

/** In dev: Vite proxy /api -> backend. In Tauri desktop: use full backend URL. */
const apiBase = import.meta.env.VITE_API_BASE || '/api'

const api = axios.create({
  baseURL: apiBase,
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

export interface ExportMusicXmlResponse {
  musicxml: string
  filename: string
  guardrail_status?: 'SAFE' | 'WARNING' | 'BLOCKED'
  error?: string
  status?: string
  reasons?: string[]
}

export async function exportMusicXml(compiled: Candidate): Promise<ExportMusicXmlResponse> {
  const { data } = await api.post<ExportMusicXmlResponse>('/export/musicxml', {
    compiled,
    filename: 'composition.musicxml',
  })
  return data
}

export async function listPresets(): Promise<string[]> {
  const { data } = await api.get<string[]>('/engines/presets')
  return Array.isArray(data) ? data : []
}

export async function listEngines(): Promise<string[]> {
  const { data } = await api.get<string[]>('/engines')
  return Array.isArray(data) ? data : []
}

export interface EngineRoles {
  form_engine?: string
  harmony_engine?: string
  texture_engine?: string
  orchestration_engine?: string
  counterpoint_engine?: string
}

export interface HybridGenerateRequest {
  engine_roles: EngineRoles
  parameters?: { input_text?: string; seed?: number; count?: number; finalist_count?: number }
}

export interface HybridGenerateResponse {
  candidates: Candidate[]
  ranked: Candidate[]
  finalists: Candidate[]
}

export async function generateHybrid(
  req: HybridGenerateRequest
): Promise<HybridGenerateResponse> {
  const { data } = await api.post<HybridGenerateResponse>('/hybrid/generate', req)
  return data
}

export interface ValidationResult {
  valid: boolean
  block_export: boolean
  status: 'SAFE' | 'WARNING' | 'BLOCKED'
  reasons: string[]
  details: Record<string, unknown>
}

export async function validateCandidate(candidate: Candidate): Promise<ValidationResult> {
  const { data } = await api.post<ValidationResult>('/validation/export', {
    candidate,
  })
  return data
}
