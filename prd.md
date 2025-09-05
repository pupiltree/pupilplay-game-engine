# PupilPlay PRD V.1

## 1. Executive Summary
PupilPlay is the Gap-to-Game Engine of PupilTree.ai. It converts assessment-identified gaps into curriculum-aligned games, closing the loop between Assess → Play → Mastery → Insight.

## 2. Objectives
* Transform gaps into adaptive games.
* Integrate tightly with PupilAssess, PupilTeach, PupilLearn.
* Scale via Marketplace with safety and governance.
* Ensure accessibility, offline readiness, and performance.

## 3. Ecosystem Linkages
Content Engine (single source of truth) → PupilAssess (gap detection) → PupilPlay (game remediation) → PupilLearn/PupilTeach (delivery) → PupilAssess (telemetry feedback).

## 4. Gameplay Modes
Toy • Practice • GameWork • Quests • Test • Tournaments (single/multi-player).

## 5. Advanced Features
AI-assisted game creation • Adaptive difficulty • Telemetry • Emotion-aware (opt-in) • Accessibility • Offline-first • Multiplayer netcode • Stake/reward loops • Parental view • Cross-subject fusion games.

## 6. End-to-End Workflow (Gap-to-Game)
1.  **Assessments/Classwork generate responses** (PupilAssess).
2.  **Gap Detection** tags micro-concepts and error patterns.
3.  **Gap→Game Orchestrator** selects a best-fit template.
4.  **Content Fetch** pulls verified items from the Content Engine.
5.  **Game Assembly** builds a playable scene with rules, hints, and scoring.
6.  **Moderation** (for UGC) runs AI filters + human review.
7.  **Delivery** across modes (Toy/Practice/GameWork/Quest/Test/Tournament; single/multi; offline cache).
8.  **Telemetry capture** (accuracy, time, retries, hints, emotion cues).
9.  **Feedback loops** update learner model, recommendations, teacher insight, and content tuning.

## 7. Gaming Engine Mechanics
Templates (~25) with JSON schemas • Content→Game Compiler • Rules/Scoring Engine • Template state machines • Physics/simulation layer (`Phaser.js`/`Unity WebGL`) • Adaptive loop (IRT/Elo) • Hint/Socratic engine • Event bus • Multiplayer netcode • Persistence & resume • Safety/moderation pipeline.

## 8. Technical Architecture & Tech Stack
* **Frontend**: React (teachers), Flutter (students), `Phaser.js`/`Unity WebGL` (games).
* **Backend**: FastAPI (APIs), `Node.js` (realtime), Redis (cache/pub-sub), Kafka (events).
* **Data**: PostgreSQL (metadata), MongoDB (states), ClickHouse/BigQuery (analytics), OpenSearch (search).
* **AI**: LangGraph orchestration; LLMs for hints; classifiers for safety; IRT for difficulty.
* **Infra**: Kubernetes (GCP/AWS), CDN, GitHub Actions CI/CD, Observability (OTel, Prometheus/Grafana), Sentry.
* **Security/Compliance**: OAuth2/JWT, TLS, KMS at-rest encryption, COPPA/GDPR, WCAG 2.1 AA.
* **Performance**: <150ms p95 single; <250ms p95 multi; <2.5s TTFP on 4G; 50k CCU scaling.

## 9. Marketplace Design & Governance
**Lifecycle**: Creation → Validation → Moderation (AI + Human) → Publish → Discovery (filters/search/recs) → Ratings & Reviews (abuse filters, weighted ratings) → Incentives (badges/XP/credits) → Governance (reporting, escalation, audits, privacy).

## 10. Rollout Roadmap (180 Days)
* **Phase 1 (0–60)**: Core engine (Toy/Practice/Test), NCERT alignment, telemetry basics.
* **Phase 2 (60–120)**: Quests, GameWork, Multiplayer, Marketplace beta.
* **Phase 3 (120–180)**: Tournaments, advanced dashboards, offline mode, creator incentives.

## 11. Success Metrics
* Gap-closure within 2 play cycles
* Daily/weekly engagement
* Teacher adoption of GameWork
* Marketplace growth/ratings
* Test score improvement
* Emotional engagement metrics

## 12. Risks & Mitigations
* **Over-gamification** → time gates
* **Marketplace abuse** → AI + human review
* **Bandwidth** → offline-first
* **Teacher hesitation** → incentives/training
* **Engagement fade** → seasonal quests/tournaments
