-- Lugha Postgres schema (SPEC-00). Verified lesson bank + per-learner state.

CREATE TABLE learners (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL CHECK (char_length(name) BETWEEN 1 AND 40),
  is_child    BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- VERIFIED lesson bank: reviewed core content (NOT live-generated for fundamentals).
CREATE TABLE lesson_items (
  id            TEXT PRIMARY KEY,
  skill         TEXT NOT NULL CHECK (skill IN ('listening','speaking','reading','writing')),
  level         INT  NOT NULL CHECK (level >= 1),
  arabic        TEXT NOT NULL,          -- Fusha, with harakat
  translit      TEXT NOT NULL,
  meaning       TEXT NOT NULL,
  verified      BOOLEAN NOT NULL DEFAULT FALSE,  -- human-checked diacritics/grammar
  freq_rank     INT                              -- for high-frequency-first ordering
);

-- Per-learner progress + spaced-repetition schedule (SPEC-05).
CREATE TABLE progress (
  learner_id    TEXT NOT NULL REFERENCES learners(id),
  item_id       TEXT NOT NULL REFERENCES lesson_items(id),
  srs_step      INT  NOT NULL DEFAULT 0,
  due_date      DATE NOT NULL DEFAULT CURRENT_DATE,
  last_correct  BOOLEAN,
  PRIMARY KEY (learner_id, item_id)
);

-- Per-skill level per learner (drives i+1).
CREATE TABLE skill_level (
  learner_id    TEXT NOT NULL REFERENCES learners(id),
  skill         TEXT NOT NULL CHECK (skill IN ('listening','speaking','reading','writing')),
  level         INT  NOT NULL DEFAULT 1 CHECK (level >= 1),
  PRIMARY KEY (learner_id, skill)
);

-- Quiz results (rolling signal; SPEC-04).
CREATE TABLE quiz_results (
  id            BIGSERIAL PRIMARY KEY,
  learner_id    TEXT NOT NULL REFERENCES learners(id),
  skill         TEXT NOT NULL,
  percent       NUMERIC(5,2) NOT NULL CHECK (percent BETWEEN 0 AND 100),
  taken_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Gamification (SPEC-08).
CREATE TABLE badges (
  learner_id    TEXT NOT NULL REFERENCES learners(id),
  badge_key     TEXT NOT NULL,
  earned_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (learner_id, badge_key)
);
