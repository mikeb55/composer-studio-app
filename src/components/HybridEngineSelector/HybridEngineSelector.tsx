import './HybridEngineSelector.css'

export type EngineRole =
  | 'form_engine'
  | 'harmony_engine'
  | 'texture_engine'
  | 'orchestration_engine'
  | 'counterpoint_engine'

export interface EngineRoles {
  form_engine: string
  harmony_engine: string
  texture_engine: string
  orchestration_engine: string
  counterpoint_engine: string
}

const ROLE_LABELS: Record<EngineRole, string> = {
  form_engine: 'Form Engine',
  harmony_engine: 'Harmony Engine',
  texture_engine: 'Texture Engine',
  orchestration_engine: 'Orchestration Engine',
  counterpoint_engine: 'Counterpoint Engine',
}

const DEFAULT_ENGINES: EngineRoles = {
  form_engine: 'wayne_shorter',
  harmony_engine: 'wheeler_lyric',
  texture_engine: 'ligeti_texture',
  orchestration_engine: 'big_band',
  counterpoint_engine: '',
}

export interface HybridEngineSelectorProps {
  engines: string[]
  roles: Partial<EngineRoles>
  onChange: (roles: EngineRoles) => void
}

export function HybridEngineSelector({
  engines,
  roles,
  onChange,
}: HybridEngineSelectorProps) {
  const current = { ...DEFAULT_ENGINES, ...roles }

  const handleChange = (role: EngineRole, value: string) => {
    onChange({ ...current, [role]: value })
  }

  return (
    <div className="hybrid-engine-selector">
      <h3 className="hybrid-engine-selector-title">Engine Roles</h3>
      <div className="hybrid-engine-selector-grid">
        {(Object.keys(ROLE_LABELS) as EngineRole[]).map((role) => (
          <div key={role} className="hybrid-engine-selector-row">
            <label htmlFor={role}>{ROLE_LABELS[role]}</label>
            <select
              id={role}
              value={current[role] || ''}
              onChange={(e) => handleChange(role, e.target.value)}
            >
              <option value="">— None —</option>
              {engines.map((eng) => (
                <option key={eng} value={eng}>
                  {eng}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    </div>
  )
}
