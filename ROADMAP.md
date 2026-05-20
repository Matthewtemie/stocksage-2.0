# StockSage 2.0 — Project Roadmap

A 10-week (calendar 14–20 week) plan to take StockSage from a working ML project
to a production-grade system with full MLOps. Every phase builds on the previous
one.

---

## Week 1 — Refactor & foundation

**Goal:** Same project, better bones. No new ML, no new tools beyond setup.

- Day 1: Repo cloned out of OneDrive, venv with Python 3.11, package skeleton,
  `pyproject.toml`, pre-commit hooks, code quality tools auto-running, code
  inventory in `NOTES.md`
- Day 2: Move `_legacy/data_pipeline.py` constants and Alpaca client into
  `src/stocksage/config.py` and `src/stocksage/data/fetch.py`
- Day 3: Move feature engineering into `src/stocksage/features/build_features.py`
  — split the 100-line `engineer_features()` god function into ~13 small
  functions, one per feature
- Day 4: Move model training into `src/stocksage/models/train.py`, prediction
  into `src/stocksage/models/predict.py`, email logic into
  `src/stocksage/notifications/email.py`
- Day 5: Move Flask app into `src/stocksage/api/app.py`, update `run.py`
  orchestrator, end-to-end test that the new structure works locally
- Day 6: README with architecture diagram, write the #BuildInPublic post for
  the week, delete `_legacy/` folder once everything's verified

**Deliverable:** You can run training and the Flask app from the new `src/`
structure, and everything is committed/pushed.

---

## Week 2 — Testing

**Goal:** Get to ~60% test coverage. Catch regressions automatically.

- Learn pytest fundamentals (fixtures, parametrize, mocking)
- Write tests for `data/fetch.py` — mock the Alpaca API so tests run without
  internet
- Write tests for `features/build_features.py` — feed it known input, assert
  known output (this is where bugs hide)
- Write tests for `models/predict.py`
- Add Pandera schemas to validate that incoming Alpaca data has the right
  columns, types, and ranges
- Set up `pytest --cov` to measure coverage

**Deliverable:** `pytest` runs in <30 seconds and gives you a coverage report.

---

## Week 3 — MLflow

**Goal:** Stop losing track of which model performed best with which
hyperparameters.

- Learn MLflow's three concepts: tracking, projects, model registry
- Wrap `models/train.py` with MLflow logging — params, metrics (MAE, RMSE, R²,
  MAPE, Huber loss), the model itself, diagnostic plots
- Run a small hyperparameter sweep across your 3 algorithms × 6 stocks
- Compare runs in the MLflow UI (`mlflow ui` in a browser)
- Register your best model per stock in MLflow's Model Registry with a
  "Staging" tag

**Deliverable:** Screenshots of MLflow UI showing experiment comparison; one
model in registry per stock.

---

## Week 4 — DVC

**Goal:** Make the whole pipeline reproducible by anyone who clones the repo.

- Learn DVC's mental model: Git for data
- Set up a DVC remote on Google Drive (free)
- Version your data: `dvc add data/raw/`, `dvc add models/`
- Convert your training process into a DVC pipeline in `dvc.yaml`:
  fetch → preprocess → features → train → evaluate
- Run `dvc repro` to confirm reproducibility

**Deliverable:** Anyone cloning your repo can run `dvc repro` and get the exact
same models.

---

## Week 5 — Proper backtesting (the most important week)

**Goal:** Test how your models would actually perform in production, not on
data leakage.

- Learn time-series cross-validation (why random train/test splits leak)
- Learn finance metrics: Sharpe ratio, max drawdown, alpha vs. beta, log vs.
  simple returns
- Build a walk-forward backtester in `src/stocksage/backtesting/walk_forward.py`
  — train on months 1-12, predict month 13, slide forward, repeat
- Compute Sharpe, max drawdown, win rate
- Compare against buy-and-hold baseline
- Visualize equity curves

**Deliverable:** A backtest report showing realistic performance numbers
(likely worse than your current MAE suggests — that's the point).

---

## Week 6 — CI with GitHub Actions

**Goal:** Every push to GitHub gets automatically tested.

- Learn GitHub Actions syntax (jobs, steps, triggers, secrets)
- Write `.github/workflows/ci.yml` that runs pytest on every push and PR
- Add a step that runs `dvc repro --dry` to catch broken pipelines
- Add status badges to your README
- Intentionally break a test, push, see it fail, fix it, see it pass

**Deliverable:** Green CI badge on your README.

---

## Week 7 — Docker

**Goal:** "Works on my machine" → "works anywhere."

- Learn Docker fundamentals (images vs. containers, Dockerfile, layer caching,
  multi-stage builds)
- Write a Dockerfile for the Flask API — multi-stage build, keep image under
  ~300MB
- Use `docker-compose` for local dev with MLflow tracking server included
- Push the image to GitHub Container Registry (ghcr.io)
- Configure Render to pull from there

**Deliverable:** `docker run stocksage` starts the app on any machine with
Docker.

---

## Week 8 — Automated retraining (the moneymaker week)

**Goal:** The system retrains itself when conditions warrant.

- Learn webhooks and Render's deploy hooks
- Read MLflow's Model Registry webhooks docs
- Write `.github/workflows/retrain.yml` that runs weekly (or on data drift
  trigger):
  1. Pulls fresh data via Alpaca
  2. Runs `dvc repro`
  3. Logs run to MLflow
  4. If new model beats current Production model on backtest metrics, promotes
     it in the registry
  5. Triggers a Render redeploy via webhook

**Deliverable:** You can sit back and the system updates itself; you'll feel
like a real ML engineer.

---

## Week 9 — Drift monitoring

**Goal:** Know when your model's predictions stop matching reality.

- Learn two statistical tests: Kolmogorov-Smirnov (compare distributions) and
  PSI (industry standard for feature drift in finance)
- Implement drift checks in `src/stocksage/monitoring/drift.py`
- Log predictions to SQLite (Render ephemeral storage is fine for now; swap
  for Postgres later)
- Build a Streamlit dashboard showing:
  - Feature drift over time
  - Prediction distribution over time
  - Live performance vs. backtest performance
- Deploy the Streamlit app as a separate service on Render

**Deliverable:** Live monitoring dashboard at
`https://stocksage-monitor.onrender.com`.

---

## Week 10 — Polish & ship

**Goal:** Make the work findable and impressive.

- Write a real README with architecture diagram (use Mermaid or draw.io)
- Record a 3-minute Loom walkthrough showing the system in action
- Write the #BuildInPublic finale post for X/LinkedIn
- Write a longer blog post: "How I rebuilt my ML project as a production
  system — 10 weeks of MLOps from scratch"
- Update your portfolio site
- Add the project to your resume with a one-line description for each MLOps
  capability

**Deliverable:** Portfolio-grade project that you can point to in interviews.

---

## Pacing reality check

At ~30–60 min per weekday with public daily commits, each "week" above is
roughly **calendar 1.5–2 weeks**. So the full project is realistically
**14–20 calendar weeks** end to end. Slippage is normal; structure matters
more than the timeline.

A few honest pacing notes:

- **Weeks 1–2 are the slowest in terms of visible progress.** Refactoring and
  testing don't *look* like much, but every later week gets dramatically
  faster because of them.
- **Week 5 (backtesting) is the steepest learning curve.** Budget extra time.
  The finance concepts are new even for experienced ML engineers.
- **Week 8 (automated retraining) is the highest-leverage week for portfolio
  impact.** That's the one that makes recruiters go "oh, this person actually
  knows MLOps."
- **Week 10 polish is non-optional.** Projects nobody knows about don't get
  jobs.

---

## When to ask for help

- You hit an error you can't decode in 15 minutes
- You're unsure where a piece of code belongs in the structure
- A weekly sanity check before moving to the next phase
- Reviewing architecture decisions before you commit to them
- Stuck on a concept (ask for an analogy, not just the answer)

## When NOT to ask for help

- For implementing something you can clearly see how to do
- For boilerplate code you can copy from docs
- After every small step — bundle questions when possible

The actual building should be you. That's where the learning lives.
