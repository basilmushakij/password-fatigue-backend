# AI Password Risk Detection

A small web app that estimates how risky a password is, using only **how it is typed on a keyboard**.
It does not look at a list of leaked passwords. It looks at patterns such as keys that sit next to each other
(`qwerty`, `asdf`, `1234`) and repeated characters.

This is a **mini project** from my course. I presented it to my instructor under the title *AI Password Risk Detection*
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

## What "risk" means here
"Risk" in this project means **how lazy the typing pattern looks** (keys next to each other, many repeats), not how strong the password is in general.
A password like `password` is very common, but it is not typed in a lazy pattern on the keyboard, so the model does not call it High.

A few passwords I tried by hand (not a measured accuracy, just examples to show what the model looks at):

| Password | Risk level |
|----------|-----------|
| `qwerty`, `123456`, `aaaaaa` | 0 (High) |
| `password`, `Summer2024` | 1 (Medium) |
| `Xk9#mP2$vL7q` | 2 (Low) |

If I continued this project, I would add a list of common passwords as an extra feature, so that words like `password` are caught too.

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

The password must be 1-128 characters. Anything else (empty, too long, missing field) gets HTTP 422 and never reaches the model.

### Tests
```bash
cd backend
pip install pytest httpx   # plus requirements.txt
python -m pytest -q
```
6 tests cover `/health`, a normal `/predict`, the three kinds of bad input, and the CORS rule.

## Project layout
```text
backend/
  main.py          FastAPI app (/health, /predict)
  model_logic.py   Keyboard map and feature extraction
  test_api.py      Tests for the API
  model/model.pkl  Trained model
frontend/src/
  index.html       Single static page, no build step
docker-compose.yml
```

## Key finding about the accuracy
In our class notebook the model scored **99.72% on the test set (100% on the training set)**, using a 30,008-row dataset made for the project.
That dataset is not a set of real leaked passwords, and I never checked its labels against real password strength.
So the number shows that the model fits the dataset's rule, not that it can find weak real-world passwords. I do not use 99.72% as a measure of real accuracy.

## Limitations
- **The training script and training data are not in this repo**, only the trained model file. I can't show here how the model was trained,
  so treat the output as a rough indication, not a security guarantee.
- It only measures typing patterns. A password can look "Medium" or "Low" here and still be weak (for example `password`, a very common word
  whose keys are far apart) or be already leaked.
- Only an English QWERTY layout is supported.
- `model.pkl` is a pickle file (loaded with `joblib`). Loading pickle files from other people can run code, so only load models you trust.
  `scikit-learn` is pinned to 1.6.1 because the model was saved with that version.

## Security notes
This is a demo, not a production service:
- Do **not** type a real password. It is sent to the backend as plain text over HTTP, and the frontend is hard-coded to `http://localhost:8000`.
- CORS only allows the demo frontend (`http://localhost:4000`). There is no login or rate limit.
