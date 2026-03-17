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

// --- Playback ---

export interface PlaybackStatus {
  status: string
  state?: 'stopped' | 'playing' | 'paused'
  message?: string
  file_path?: string
  loop_start?: number
  loop_end?: number
}

export async function playbackPlay(params: {
  file_path?: string
  musicxml?: string
  loop_start?: number
  loop_end?: number
}): Promise<PlaybackStatus> {
  const { data } = await api.post<PlaybackStatus>('/playback/play', params)
  return data
}

export async function playbackStop(): Promise<PlaybackStatus> {
  const { data } = await api.post<PlaybackStatus>('/playback/stop')
  return data
}

export async function playbackPause(): Promise<PlaybackStatus> {
  const { data } = await api.post<PlaybackStatus>('/playback/pause')
  return data
}

export async function playbackLoop(loop_start?: number, loop_end?: number): Promise<PlaybackStatus> {
  const { data } = await api.post<PlaybackStatus>('/playback/loop', {
    loop_start,
    loop_end,
  })
  return data
}

export async function playbackStatus(): Promise<PlaybackStatus> {
  const { data } = await api.get<PlaybackStatus>('/playback/status')
  return data
}

// --- Project ---

export interface ProjectCreateResponse {
  project_name: string
  path: string
}

export interface ProjectRunResponse {
  run_path: string
  run_label: string
}

export interface RunHistoryEntry {
  run_label: string
  run_path: string
  preset_name?: string
  input_text?: string
  seed?: number
  timestamp?: string
  candidates?: unknown[]
  selected_candidate?: unknown
  export_paths?: string[]
}

export interface ProjectDetail {
  project_name: string
  path: string
  runs: RunHistoryEntry[]
}

export async function createProject(projectName: string): Promise<ProjectCreateResponse> {
  const { data } = await api.post<ProjectCreateResponse>('/project', {
    project_name: projectName,
  })
  return data
}

export async function saveRunToProject(params: {
  project_name: string
  run_label?: string
  preset_name?: string
  engine?: string
  input_text?: string
  seed?: number
  candidates?: Candidate[]
  selected_candidate?: Candidate
  export_paths?: string[]
  musicxml?: string
}): Promise<ProjectRunResponse & { metadata_path?: string; export_paths?: string[] }> {
  const { data } = await api.post('/project/run/save', params)
  return data
}

export async function getProjectHistory(projectName: string): Promise<RunHistoryEntry[]> {
  const { data } = await api.get<RunHistoryEntry[]>(`/project/history/${encodeURIComponent(projectName)}`)
  return data
}

export async function getProject(projectName: string): Promise<ProjectDetail> {
  const { data } = await api.get<ProjectDetail>(`/project/${encodeURIComponent(projectName)}`)
  return data
}

export async function listProjects(): Promise<string[]> {
  const { data } = await api.get<string[] | { projects?: string[] }>('/project')
  const arr = Array.isArray(data) ? data : (data as { projects?: string[] })?.projects ?? []
  return arr
}
