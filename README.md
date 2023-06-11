# Cassandra distributed database cinema application
## Set-up
1. Create a `Python 3.8` virtual environment.
2. Activate it.
3. Install the dependencies.
```shell
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the database:
```shell
docker-compose up -d && ./scripts/initialize.sh
```

Start the application:
```shell
python main.py
```

## File structure
```
.
├── main.py                   # Application
├── utils.py                  # Functions
├── tests                     # Test files
│   └── stress_tests.py       # Stress tests
├── scripts                   # Test files
│   ├── initialize.sh         # Wait for the cluster to load
│   │                           and start DB initialization
│   └── init-db.cql           # Build the initial DB
├── docker-compose.yml        # Docker-compose cluster
├── requirements.txt          # Dependencies
└── README.md
```

## Clean-up
To remove the database:
```shell
docker-compose down --volumes
```
