# NBA Winner Predictor

An end-to-end machine learning project that predicts the winner of upcoming NBA games and displays each game's win probability in a web dashboard.

The MVP focuses on predicting the **home team's win probability** before tip-off. The system is designed to start simple with historical team-level data and baseline models, then improve over time with lineup, injury, player-availability, and model-calibration features.

> This project is for machine learning and forecasting practice. It is not betting advice.

---

## Project Goal

The goal is to build a full-stack ML system that can:

1. Collect historical NBA game data.
2. Build pre-game features without data leakage.
3. Train and evaluate several classification models.
4. Generate predictions for upcoming games.
5. Serve predictions through an API.
6. Display predictions in a React dashboard.

The target variable is:

```text
home_win = 1 if home_score > away_score else 0
home_win = 0 otherwise
```

The main prediction output is:

```text
P(home team wins)
P(away team wins) = 1 - P(home team wins)
```

---

## How It Works

At a high level, the system follows this pipeline:

```text
[Data Sources]
  nba_api / NBA stats / schedule source / lineup and injury source
        |
        v
[Ingestion Jobs]
  historical backfill + scheduled game-day snapshots
        |
        v
[Storage Layer]
  raw snapshots + normalized database tables
        |
        v
[Feature Pipeline]
  rolling stats, rest days, home/away, matchup, injury, lineup features
        |
        v
[Model Training]
  baselines, logistic regression, tree models, random forest, boosting later
        |
        v
[Prediction Service]
  FastAPI or Flask API returns current predictions
        |
        v
[React Dashboard]
  today's games, win probabilities, model version, prediction timestamp
```

The most important design principle is that every feature must represent information available **before the game starts**. For example, rolling team averages should only use games played before the target game. Final score, post-game box score values, or confirmed information that was not available at prediction time should never be used as model input.

---

## MVP Features

The first version should use mostly team-level and schedule-based features because they are easier to collect reliably.

Recommended initial feature set:

```text
home_team_rolling_win_pct_10
away_team_rolling_win_pct_10
rolling_win_pct_diff

home_team_rolling_point_diff_10
away_team_rolling_point_diff_10
rolling_point_diff_diff

home_team_rolling_pts_for_10
away_team_rolling_pts_for_10

home_team_rolling_pts_allowed_10
away_team_rolling_pts_allowed_10

home_rest_days
away_rest_days
home_back_to_back
away_back_to_back

home_top_player_out_count
away_top_player_out_count
starter_confirmed_flag
```

Later versions can add more advanced player-level features, such as minutes-weighted injury impact, expected starter strength, bench strength, and top-player availability.

---

## Recommended Tech Stack

### Backend and ML

- Python
- pandas
- scikit-learn
- nba_api
- XGBoost or LightGBM later
- MLflow for experiment tracking
- FastAPI or Flask for the prediction API

### Frontend

- React
- Vite or Next.js
- Dashboard components for games, probabilities, timestamps, and model metadata

### Storage

- PostgreSQL, Supabase, or RDS for structured tables
- S3-compatible object storage for raw immutable snapshots
- Parquet files for training-ready feature datasets

### Deployment

- Frontend: Vercel or Netlify
- Backend: Render, Railway, Fly.io, AWS ECS, or Lambda container
- Scheduled jobs: GitHub Actions, AWS EventBridge, cron, or a managed worker

---

## Repository Structure

```text
nba-winner-predictor/
  README.md
  .env.example
  docker-compose.yml
  requirements.txt or pyproject.toml

  data/
    raw/                  # local development only; do not commit full raw data
    processed/            # local feature files or samples

  notebooks/              # exploration only

  src/
    config.py

    ingestion/
      nba_api_client.py
      lineup_scraper.py
      injury_scraper.py
      backfill_games.py
      scheduled_snapshot.py

    storage/
      s3_client.py
      db.py
      schemas.sql

    features/
      build_team_features.py
      build_player_features.py
      build_game_features.py
      leakage_checks.py

    models/
      train.py
      evaluate.py
      calibrate.py
      predict.py
      registry.py

    api/
      app.py
      routes.py
      services.py

    utils/
      logging.py
      time.py

  frontend/
    src/
      pages/
      components/
      api/
      styles/

  tests/
    test_features_no_leakage.py
    test_ingestion_schema.py
    test_api_predictions.py
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/nba-winner-predictor.git
cd nba-winner-predictor
```

### 2. Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

A starting `requirements.txt` could include:

```text
pandas
numpy
scikit-learn
nba_api
sqlalchemy
psycopg2-binary
fastapi
uvicorn
mlflow
python-dotenv
requests
beautifulsoup4
```

### 4. Create environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Example `.env.example`:

```text
DATABASE_URL=postgresql://user:password@localhost:5432/nba_predictor
S3_BUCKET=nba-predictor
MODEL_PATH=models/latest_model.pkl
ENV=development
```

---

## Data Pipeline

### Historical Backfill

The historical backfill collects past NBA games and stores both raw and normalized versions.

Expected output:

- Game IDs
- Game dates
- Home and away teams
- Scores
- Team stats
- Player stats, if included
- `home_win` label

Example command:

```bash
python -m src.ingestion.backfill_games --start-season 2015 --end-season 2025
```

### Raw Snapshot Storage

Raw data should be saved before transformation so the pipeline is reproducible.

Example path:

```text
s3://nba-predictor/raw/nba_api/date=2026-05-25/games.json
```

For local development:

```text
data/raw/nba_api/date=2026-05-25/games.json
```

### Normalized Tables

Suggested database tables:

```text
games
team_game_stats
player_game_stats
lineup_snapshots
injury_snapshots
feature_rows
predictions
```

---

## Feature Engineering

The feature pipeline creates one row per game. Each row should contain only information that would have been available before that game.

Example command:

```bash
python -m src.features.build_game_features --feature-version v1
```

Important checks:

- Rolling averages must shift by one game so the target game is excluded.
- Feature rows should not include final score-derived fields from the same game.
- Injury and lineup snapshots should include a `collected_at_utc` timestamp.
- Prediction rows should reference the snapshot used to create them.

---

## Modeling

This project should start with simple baselines before using more complex models.

Recommended model order:

1. Home-team baseline
2. Elo-style rating baseline
3. Logistic regression
4. Decision tree
5. Random forest
6. Gradient boosting / XGBoost / LightGBM
7. Small neural network only after tabular baselines are strong

Example training command:

```bash
python -m src.models.train --feature-version v1 --model logistic_regression
```

Example evaluation command:

```bash
python -m src.models.evaluate --model-version latest
```

### Evaluation Metrics

Use a time-based split instead of a random split. A realistic split could be:

```text
Train:      2015-2023 seasons
Validation: 2023-2024 season
Test:       2024-2025 season
```

Track these metrics:

- Accuracy
- Log loss
- Brier score
- ROC-AUC
- Calibration curve

Accuracy is easy to understand, but it is not enough. Since the dashboard displays probabilities, log loss, Brier score, and calibration are especially important.

---

## Live Prediction Pipeline

On game days, the system should:

1. Pull today's or tomorrow's NBA schedule.
2. Collect lineup and injury snapshots from allowed sources.
3. Build feature rows for upcoming games.
4. Load the latest trained model.
5. Save predictions to the database.
6. Expose predictions through the API.

Example command:

```bash
python -m src.ingestion.scheduled_snapshot
python -m src.models.predict --date today
```

Each prediction should include:

```text
game_id
home_team
away_team
home_win_prob
away_win_prob
predicted_at_utc
model_version
feature_version
input_snapshot_id
stale_data_flag
```

---

## API Design

The backend can be built with FastAPI or Flask.

Recommended endpoints:

```text
GET /health
GET /games/today
GET /predictions/today
GET /predictions/{game_id}
GET /model/metadata
```

Example prediction response:

```json
{
  "game_id": "0022500001",
  "home_team": "BOS",
  "away_team": "NYK",
  "home_win_prob": 0.64,
  "away_win_prob": 0.36,
  "predicted_at_utc": "2026-05-25T18:30:00Z",
  "model_version": "random_forest_v1",
  "feature_version": "v1",
  "lineup_status": "projected",
  "stale_data_flag": false
}
```

Run the API locally:

```bash
uvicorn src.api.app:app --reload
```

---

## Frontend Dashboard

The React dashboard should show:

- Today's games
- Home and away teams
- Home win probability
- Away win probability
- Model version
- Prediction timestamp
- Lineup status: projected or confirmed
- Stale-data warning when inputs are old

Example dashboard card:

```text
Knicks @ Celtics
Celtics win probability: 64%
Knicks win probability: 36%
Model: random_forest_v1
Prediction time: 2026-05-25 6:30 PM UTC
Lineups: Projected
```

Run the frontend locally:

```bash
cd frontend
npm install
npm run dev
```

---

## Roadmap

### Phase 0: Setup

- Create GitHub repository
- Add `.env.example`
- Create Python environment
- Add React frontend folder
- Add Dockerfile and optional `docker-compose.yml`

### Phase 1: Historical Data

- Pull historical game logs with `nba_api`
- Save raw snapshots
- Normalize games into database tables
- Create `home_win` labels

### Phase 2: Features

- Create one row per game
- Add rolling team features
- Add rest-day and back-to-back features
- Add home/away and matchup-difference features
- Add leakage tests

### Phase 3: Modeling

- Train home-team baseline
- Train Elo baseline
- Train logistic regression
- Train decision tree and random forest
- Add gradient boosting after MVP baseline works
- Evaluate with time-based splits

### Phase 4: Live Prediction

- Pull today/tomorrow schedule
- Snapshot lineups and injuries
- Build feature rows for upcoming games
- Load latest model
- Save predictions

### Phase 5: API

- Build `/health`
- Build `/games/today`
- Build `/predictions/today`
- Build `/predictions/{game_id}`
- Build `/model/metadata`

### Phase 6: Frontend

- Show today's games
- Show win probabilities
- Show model version and prediction timestamp
- Show lineup and injury data status
- Add loading, error, and stale-data states

### Phase 7: Deployment

- Deploy frontend
- Deploy backend
- Set up PostgreSQL
- Set up object storage
- Schedule ingestion every 30-60 minutes on game days

---

## First Two-Week Plan

### Days 1-2

- Create repo
- Set up Python environment
- Add Docker setup
- Create README skeleton
- Draft database schema
- Create source adapter interfaces

### Days 3-5

- Backfill historical games using `nba_api`
- Store raw files
- Normalize games and team stats

### Days 6-7

- Create first feature table
- Add rolling win percentage
- Add rolling point differential
- Add rest days
- Add home/away features

### Days 8-9

- Train home baseline
- Train logistic regression
- Train decision tree
- Train random forest
- Use time-based split

### Days 10-11

- Create evaluation report
- Track accuracy, log loss, Brier score, ROC-AUC, and calibration

### Days 12-14

- Build simple API endpoint
- Save predictions from a trained model
- Build a basic React dashboard page

---

## Testing Strategy

Recommended tests:

```text
test_features_no_leakage.py
  Confirms rolling features do not include the target game.

test_ingestion_schema.py
  Confirms raw and normalized data match expected columns.

test_api_predictions.py
  Confirms prediction endpoints return valid probabilities and metadata.
```

Useful validation rules:

- `home_win_prob` must be between 0 and 1.
- `away_win_prob` should equal `1 - home_win_prob`.
- Every prediction must have a model version.
- Every prediction must have a timestamp.
- Every feature row must have a feature version.

---

## Limitations

NBA predictions are noisy because player availability, rest, matchup context, and late lineup changes can strongly affect outcomes. A model trained only on historical team stats may perform reasonably as a learning project, but it will likely struggle when stars are unexpectedly ruled out or teams rest players.

The dashboard should clearly show when predictions were generated and whether lineup or injury data was projected or confirmed.

---

## Future Extensions

- Player-level injury impact weighting
- XGBoost or LightGBM tuning
- MLflow model registry
- SHAP explanations
- Odds and spread comparison
- Spread regression model
- React Native mobile app
- Backtesting against market odds
- Separate regular-season and playoff models

---

## License

Add a license before publishing the repository. For a personal portfolio project, MIT is a common choice.
