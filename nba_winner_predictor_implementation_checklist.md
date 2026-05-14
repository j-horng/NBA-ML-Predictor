# NBA Winner Predictor — Implementation Checklist

## MVP Objective
Build an end-to-end ML system that predicts the home-team win probability for upcoming NBA games and displays predictions in a React dashboard.

## Phase 0 — Setup
- [ ] Create GitHub repo: `nba-winner-predictor`
- [ ] Add `.env.example` for API keys, database URL, S3 bucket, model path
- [ ] Create Python environment with `nba_api`, `pandas`, `scikit-learn`, `sqlalchemy`, `fastapi` or `flask`, `mlflow`
- [ ] Create React frontend folder
- [ ] Add Dockerfile and optional `docker-compose.yml`

## Phase 1 — Historical Data
- [ ] Pull historical game logs using `nba_api`
- [ ] Save raw snapshots to object storage or local `/data/raw/` during development
- [ ] Normalize games into database tables
- [ ] Create labels: `home_win = 1 if home_score > away_score else 0`

## Phase 2 — Features
- [ ] Create one row per game
- [ ] Add rolling team features using only games before the target game
- [ ] Add rest-day and back-to-back features
- [ ] Add home/away and matchup-difference features
- [ ] Add leakage tests

## Phase 3 — Modeling
- [ ] Train home-team baseline
- [ ] Train Elo/simple rating baseline
- [ ] Train logistic regression
- [ ] Train decision tree and random forest
- [ ] Add gradient boosting after MVP baseline works
- [ ] Evaluate with time-based split, not random split
- [ ] Track accuracy, log loss, Brier score, ROC-AUC, and calibration

## Phase 4 — Live Prediction Pipeline
- [ ] Pull today/tomorrow schedule
- [ ] Snapshot lineups and injuries from allowed sources
- [ ] Build feature rows for upcoming games
- [ ] Load latest model and save predictions
- [ ] Add stale-data warning when inputs are old

## Phase 5 — API
- [ ] `GET /health`
- [ ] `GET /games/today`
- [ ] `GET /predictions/today`
- [ ] `GET /predictions/{game_id}`
- [ ] `GET /model/metadata`

## Phase 6 — Frontend
- [ ] Show today’s games
- [ ] Show home and away win probabilities
- [ ] Show model version and prediction timestamp
- [ ] Show whether starters/injury data are projected or confirmed
- [ ] Add loading, error, and stale-data states

## Phase 7 — Deployment
- [ ] Deploy frontend to Vercel or Netlify
- [ ] Deploy backend to Render, Railway, Fly.io, ECS, or Lambda container
- [ ] Use PostgreSQL/Supabase/RDS for structured data
- [ ] Use S3-compatible object storage for raw snapshots
- [ ] Schedule ingestion every 30-60 minutes on game days

## Later Extensions
- [ ] Player-level injury impact weighting
- [ ] XGBoost/LightGBM tuning
- [ ] MLflow model registry
- [ ] SHAP explanations
- [ ] Odds/spread comparison
- [ ] Spread regression model
- [ ] React Native mobile app
