import { useState } from 'react'

export function ScanForm() {
  const [repositoryUrl, setRepositoryUrl] = useState('')
  const [message, setMessage] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    if (!repositoryUrl.trim()) {
      setMessage('Please enter a GitHub repository URL.')
      return
    }

    setMessage('Repository URL is ready to scan.')
  }

  return (
    <form className="scan-form" onSubmit={handleSubmit} noValidate>
      <label htmlFor="repository-url">GitHub repository URL</label>
      <div className="input-row">
        <input
          id="repository-url"
          name="repository-url"
          type="url"
          placeholder="https://github.com/owner/repository"
          value={repositoryUrl}
          onChange={(event) => setRepositoryUrl(event.target.value)}
          aria-describedby="form-message"
        />
        <button type="submit">Scan Repository</button>
      </div>
      <p id="form-message" className="form-message" role="status">
        {message}
      </p>
    </form>
  )
}
