import './GuardrailStatus.css'

export type GuardrailStatusType = 'SAFE' | 'WARNING' | 'BLOCKED'

export interface GuardrailStatusProps {
  status: GuardrailStatusType
  reasons?: string[]
  details?: Record<string, unknown>
}

export function GuardrailStatus({ status, reasons = [], details }: GuardrailStatusProps) {
  return (
    <div className={`guardrail-status guardrail-status--${status.toLowerCase()}`}>
      <span className="guardrail-status-badge">{status}</span>
      {reasons.length > 0 && (
        <ul className="guardrail-status-reasons">
          {reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      )}
      {details && Object.keys(details).length > 0 && (
        <details className="guardrail-status-details">
          <summary>Details</summary>
          <pre>{JSON.stringify(details, null, 2)}</pre>
        </details>
      )}
    </div>
  )
}
