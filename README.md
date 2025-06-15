# SnipShare API

A simple RESTful API for searching, sharing, and upvoting code snippets. Perfect for developers who want to quickly find and contribute reusable code.

**Production API Base URL:**
```
https://api.syntax-xxx.is-a.dev
```

---

## Features
- Add a new code snippet
- Search snippets by query, language, or tag
- Get a random snippet
- Upvote a snippet

---

## Endpoints

### Add a Snippet
`POST /snippets`
```json
{
  "title": "Hello World in Python",
  "code": "print('Hello, world!')",
  "language": "python",
  "tags": ["beginner", "example"]
}
```

### Search Snippets
`GET /snippets?query=...&language=...&tag=...`

### Get a Random Snippet
`GET /snippets/random`

### Upvote a Snippet
`POST /snippets/{id}/upvote`

---

## Documentation
- Interactive API docs: [`/docs`](https://SShare.api.syntax-xxx.is-a.dev/docs)
- Static info page: [`/`](https://SShare.api.syntax-xxx.is-a.dev/)
- Developer test overlay: [`/dev`](https://SShare.api.syntax-xxx.is-a.dev/dev) *(for personal testing only)*

---

## Running Locally
1. Install dependencies:
   ```sh
   pip install fastapi uvicorn sqlalchemy pydantic
   ```
2. Start the server:
   ```sh
   uvicorn main:app --reload
   ```
3. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Disclaimer
> **ALWAYS CHECK THE CODE YOU USE FOR MALICIOUS SOFTWARE. WE DO NOT GUARANTEE THAT ALL CODES ARE SAFE. IF YOU FIND MALICIOUS SOFTWARE, REPORT IT ON THE DISCORD.**

---

## Contact / Reporting
If you find malicious code or have questions, please report it on the Discord server.
