export function Loading({ label = "Caricamento..." }) {
  return (
    <div className="status" role="status">
      <span className="spinner" aria-hidden="true" />
      {label}
    </div>
  );
}

export function ErrorMessage({ error, onRetry }) {
  return (
    <div className="status status--error" role="alert">
      <span>{error?.message || "Si e' verificato un errore."}</span>
      {onRetry && (
        <button type="button" className="btn" onClick={onRetry}>
          Riprova
        </button>
      )}
    </div>
  );
}
