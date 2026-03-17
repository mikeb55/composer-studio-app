import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  listProjects,
  createProject,
  getProjectHistory,
  type RunHistoryEntry,
} from '../api/client'
import './ProjectPage.css'

export function ProjectPage() {
  const [projects, setProjects] = useState<string[]>([])
  const [selectedProject, setSelectedProject] = useState<string | null>(null)
  const [runs, setRuns] = useState<RunHistoryEntry[]>([])
  const [newProjectName, setNewProjectName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadProjects = async () => {
    try {
      const list = await listProjects()
      setProjects(Array.isArray(list) ? list : [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load projects')
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  useEffect(() => {
    if (!selectedProject) {
      setRuns([])
      return
    }
    getProjectHistory(selectedProject)
      .then((r) => setRuns(Array.isArray(r) ? r : []))
      .catch(() => setRuns([]))
  }, [selectedProject])

  const handleCreateProject = async () => {
    const name = newProjectName.trim()
    if (!name) return
    setLoading(true)
    setError(null)
    try {
      await createProject(name)
      setNewProjectName('')
      await loadProjects()
      setSelectedProject(name)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="project-page">
      <header className="project-page-header">
        <Link to="/" className="project-page-back">
          ← Back to Generate
        </Link>
        <h1>Projects</h1>
      </header>

      <section className="project-page-content">
        <div className="project-page-sidebar">
          <h2>Projects</h2>
          <div className="project-create">
            <input
              type="text"
              placeholder="New project name"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleCreateProject()}
            />
            <button
              type="button"
              onClick={handleCreateProject}
              disabled={loading || !newProjectName.trim()}
            >
              Create
            </button>
          </div>
          <ul className="project-list">
            {projects.map((p) => (
              <li key={p}>
                <button
                  type="button"
                  className={selectedProject === p ? 'selected' : ''}
                  onClick={() => setSelectedProject(p)}
                >
                  {p}
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="project-page-main">
          {error && <div className="project-error">{error}</div>}
          {selectedProject ? (
            <>
              <h2>Run History: {selectedProject}</h2>
              {runs.length === 0 ? (
                <p className="project-empty">No runs yet. Generate a composition and save it to this project.</p>
              ) : (
                <ul className="run-history">
                  {runs.map((run) => (
                    <li key={run.run_path} className="run-entry">
                      <div className="run-label">{run.run_label}</div>
                      <div className="run-meta">
                        {run.preset_name && <span>Preset: {run.preset_name}</span>}
                        {run.engine && <span>Engine: {run.engine}</span>}
                        {run.input_text && <span>Title: {run.input_text}</span>}
                        {run.timestamp && <span>{run.timestamp}</span>}
                      </div>
                      {run.export_paths && run.export_paths.length > 0 && (
                        <Link
                          to={`/score?file=${encodeURIComponent(run.export_paths[0])}`}
                          className="run-view-score"
                        >
                          View Score
                        </Link>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </>
          ) : (
            <p className="project-empty">Select a project or create one.</p>
          )}
        </div>
      </section>
    </div>
  )
}

export default ProjectPage
