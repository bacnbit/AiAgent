import { useState } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState('idle')

  const handleAnalyze = async () => {
    setStatus('analyzing')
    // TODO: Implement API call to start analysis
    console.log('Starting analysis...')
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Agent - ERP Configuration Validator</h1>
        <p>Validate ERP configurations against customer contracts</p>
      </header>

      <main className="app-main">
        <section className="analyze-section">
          <h2>Start Analysis</h2>
          <button
            className="btn-primary"
            onClick={handleAnalyze}
            disabled={status === 'analyzing'}
          >
            {status === 'analyzing' ? 'Analyzing...' : 'Analyze Contract'}
          </button>
        </section>

        <section className="status-section">
          <h3>Status: {status}</h3>
          {/* TODO: Add real-time progress display */}
        </section>

        <section className="results-section">
          <h3>Results</h3>
          {/* TODO: Add results and approval interface */}
          <p>No analysis results yet. Click "Analyze Contract" to start.</p>
        </section>
      </main>
    </div>
  )
}

export default App
