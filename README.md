# Setup
If there is not `test.db` file in root directory issue
```bash
touch test.db
```

# How to start

```bash
docker-compose up --build backend
```

# How to fetch data
```bash
curl "localhost:8000/plannings?limit=10&skip=10"  # pagination
curl "localhost:8000/plannings?sort=desc"  # sorting
curl "localhost:8000/plannings?sort=desc&filter_office_postal_code=73608"  # filtering
```