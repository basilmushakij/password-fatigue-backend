# AI Password Risk Detection

A small web app that estimates how risky a password is, using only **how it is typed on a keyboard**.
It does not look at a list of leaked passwords. It looks at patterns such as keys that sit next to each other
(`qwerty`, `asdf`, `1234`) and repeated characters.

I presented this project to my instructor under the title *AI Password Risk Detection*
(the repo is named after the idea of "password fatigue": people pick easy-to-type passwords when they are tired of making new ones).

## How it works
1. The frontend sends the typed password to the backend (`POST /predict`).
2. The backend turns the password into 4 numbers (`backend/model_logic.py`):

   | Feature | Meaning |
   |---------|---------|
   | `avg_dist` | Average distance between two neighbouring characters on a QWERTY keyboard (small = keys close together) |
   | `length` | Number of characters |
   | `unique_ratio` | Unique characters divided by length (small = lots of repeats) |
   | `seq_ratio` | Share of neighbouring pairs that are on adjacent keys (distance <= 1.3) |

3. A trained scikit-learn model (`backend/model/model.pkl`, an ensemble of tree-based classifiers) predicts a risk level:
   `0` = High, `1` = Medium, `2` = Low.
4. The page shows the risk level, the key distance and the unique ratio.

Only lower-case characters on a US QWERTY layout are mapped. Characters outside `KEY_MAP` (for example Thai letters) are skipped when measuring distance.

## Run it
You need Docker.

```bash
docker compose up --build
```
- Frontend: http://localhost:4000 (a static page served by `python -m http.server`)
- Backend API: http://localhost:8000 (FastAPI, docs at `/docs`)

### API
```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"password":"qwerty123"}'
# {"risk_level": 0, "avg_dist": ..., "unique_ratio": ...}
```

## Project layout
```text
backend/
  main.py          FastAPI app (/health, /predict)
  model_logic.py   Keyboard map and feature extraction
  model/model.pkl  Trained model
frontend/src/
  index.html       Single static page, no build step
docker-compose.yml
```

## Limitations
- **The training script and training data are not in this repo**, only the trained model file. I can't show here how the model was trained,
  and I did not measure and publish its accuracy, so treat the output as a rough indication, not a security guarantee.
- It only measures typing patterns. A password can look "Low" risk here and still be weak (for example a common word with unusual keys)
  or be already leaked.
- Only an English QWERTY layout is supported.
- `model.pkl` is a pickle file (loaded with `joblib`). Loading pickle files from other people can run code, so only load models you trust.
  `scikit-learn` is pinned to 1.6.1 because the model was saved with that version.

## Security notes
This is a demo, not a production service:
- Do **not** type a real password. It is sent to the backend as plain text over HTTP, and the frontend is hard-coded to `http://localhost:8000`.
- CORS allows every origin and there is no login or rate limit.
