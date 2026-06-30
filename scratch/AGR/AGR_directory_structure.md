AGR/
│
├── apps/                     # Deployable services
│   ├── api-gateway/
│   ├── parser-service/
│   ├── policy-engine/
│   ├── validation-service/
│   ├── simulation-service/
│   ├── artifact-generator/
│   ├── graph-service/
│   └── telemetry-service/
│
├── packages/                 # Shared libraries
│   ├── protobuf/
│   ├── sdk/
│   ├── common/
│   ├── auth/
│   ├── metrics/
│   └── config/
│
├── policies/                 # Open Policy Agent (OPA) / Rego
│   ├── architecture/
│   ├── security/
│   └── governance/
│
├── graph/
│   ├── schemas/
│   ├── migrations/
│   └── cypher/
│
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   ├── helm/
│   ├── terraform/
│   ├── spire/
│   └── monitoring/
│
├── scripts/
│
├── tests/
│   ├── integration/
│   ├── load/
│   ├── chaos/
│   └── e2e/
│
├── docs/
│
├── .github/
│
├── Makefile
├── docker-compose.yml
├── README.md
└── LICENSE