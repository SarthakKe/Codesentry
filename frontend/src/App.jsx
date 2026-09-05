import { ScanForm } from './components/ScanForm.jsx'

function App() {
  return (
    <main className="page-shell">
      <section className="scan-card" aria-labelledby="page-title">
        <p className="logo" aria-label="CodeSentry">CodeSentry <span aria-hidden="true">🛡️</span></p>
        <h1 id="page-title">Scan your repository with confidence.</h1>
        <p className="description">
          Enter a public GitHub repository URL to prepare a security scan for common code risks.
        </p>
        <ScanForm />
      </section>
    </main>
  )
}

export default App
