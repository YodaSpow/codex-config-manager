# Scratchboard contract

The package creates `<docs>/scratchboard/` with `index.html`, `sessions/YYYY-MM-DD.html`, and `state/YYYY-MM-DD.json`. State remains the source of truth; HTML is regenerated output.

The server is bound only to `127.0.0.1`, chooses an available port, sends `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`, `Pragma: no-cache`, and `Expires: 0`, and stops after 60 minutes without a board request. A health endpoint identifies the served root before reuse.

The direct canonical URL is always included in the command handoff. A host-native preview is additive: use it whenever the host exposes one, never instead of the direct link.

Captured content is escaped before rendering. Normal prose has preserved paragraphs and line breaks; text fenced with triple backticks becomes selectable code with a copy enhancement. Links are only rendered for `http`, `https`, and repo-relative URLs.
