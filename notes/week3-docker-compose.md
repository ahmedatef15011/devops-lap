# Week 3: Docker Compose - Multi-Container Applications

**Goal**: Run a multi-container application with API + Database + Web UI

**Time**: 2-3 hours

---

## What You'll Learn

- **Docker Compose**: Orchestrate multiple containers
- **Networking**: How containers communicate
- **Volumes**: Persist data across container restarts
- **Environment Variables**: Configure containers
- **Health Checks**: Monitor container health
- **Dependencies**: Control startup order

---

## Your Stack

```
┌─────────────┐     ┌──────────────┐     ┌───────────────────┐
│   FastAPI   │────▶│   MongoDB    │◀────│  Mongo Express    │
│  (port 8000)│     │ (port 27017) │     │   (port 8081)     │
│             │     │              │     │   (Web UI)        │
└─────────────┘     └──────────────┘     └───────────────────┘
```

---

## Part 1: Understanding docker-compose.yaml

### Key Concepts

```yaml
version: '3.8'  # Compose file format version

services:       # Define containers
  api:          # Service name (becomes hostname in network)
    build: .    # Build from Dockerfile in current directory
    ports:      # Port mapping: host:container
      - "8000:8000"
    environment:  # Environment variables
      - MONGODB_URL=mongodb://admin:password@mongodb:27017/
    depends_on:   # Wait for mongodb before starting
      - mongodb
    healthcheck:  # Monitor container health
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

**My Notes**:
```
# Service name (e.g., 'mongodb') becomes the hostname
# Containers can reach each other using service names
# Example: mongodb://mongodb:27017 (not localhost!)
```

---

## Part 2: Run Your Stack

### Step 1: Start Everything

```bash
cd /Users/ahmedelbehiry/Documents/DevOps/devops-lap/simple-api

# Build and start all services
docker compose up --build
```

**What happens**:
1. Docker builds your API image
2. Pulls MongoDB and Mongo Express images
3. Creates a network for all services
4. Starts containers in dependency order
5. Streams logs from all containers

### Step 2: Test Your API

**Open a new terminal** and run:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint (tracks visits in MongoDB)
curl http://localhost:8000/

# Get visit statistics
curl http://localhost:8000/stats
```

### Step 3: Access Mongo Express (Web UI)

Open in browser: http://localhost:8081

- Click on `simple_api_db` database
- Click on `visits` collection
- See your API visits stored in MongoDB!

---

## Part 3: Essential Docker Compose Commands

```bash
# Start services (rebuild if needed)
docker compose up --build

# Start in background (detached mode)
docker compose up -d

# Stop services (containers removed)
docker compose down

# Stop and remove volumes (deletes data!)
docker compose down -v

# View logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# Logs for specific service
docker compose logs -f api

# List running services
docker compose ps

# Execute command in running container
docker compose exec api /bin/sh

# Restart a service
docker compose restart api

# View resource usage
docker compose stats
```

**My Practice**:
```bash
# Try these commands and document what you observe:

# 1. Start in background
docker compose up -d

# 2. Check status
docker compose ps

# 3. View API logs
docker compose logs api

# 4. Check MongoDB logs
docker compose logs mongodb

# 5. Stop everything
docker compose down
```

---

## Part 4: Understanding Volumes

### What Are Volumes?

Volumes persist data even when containers are deleted.

```yaml
volumes:
  mongo-data:      # Named volume
    driver: local
```

**Without volumes**: If you stop MongoDB, all data is lost  
**With volumes**: Data persists across container restarts

### Test Data Persistence

```bash
# 1. Start services
docker compose up -d

# 2. Visit API to create data
curl http://localhost:8000/
curl http://localhost:8000/
curl http://localhost:8000/stats

# 3. Stop containers
docker compose down

# 4. Start again
docker compose up -d

# 5. Check stats - data is still there!
curl http://localhost:8000/stats
```

### View Volumes

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect simple-api_mongo-data

# Remove volume (deletes data!)
docker volume rm simple-api_mongo-data
```

---

## Part 5: Understanding Networks

Docker Compose automatically creates a network for your services.

### How It Works

```
Service Name = Hostname
- api can reach mongodb at: mongodb:27017
- mongo-express reaches mongodb at: mongodb:27017
```

### Test Network Connectivity

```bash
# Get a shell inside the API container
docker compose exec api /bin/sh

# Inside container, test MongoDB connection
ping mongodb       # Should resolve to MongoDB container IP
curl mongodb:27017 # Should connect (might see error, but connection works)

# Exit container
exit
```

---

## Part 6: Environment Variables

### Three Ways to Set Environment Variables

**1. In docker-compose.yaml**:
```yaml
environment:
  - MONGODB_URL=mongodb://admin:password@mongodb:27017/
```

**2. Using .env file** (create `.env` in same folder):
```bash
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=password
```

Then reference in compose:
```yaml
environment:
  - MONGO_INITDB_ROOT_USERNAME=${MONGO_ROOT_USERNAME}
```

**3. From host environment**:
```bash
export MONGO_PASSWORD=mysecret
docker compose up
```

---

## Part 7: Health Checks

Health checks monitor if containers are working properly.

### View Health Status

```bash
# Start services
docker compose up -d

# Check health status
docker compose ps

# You'll see health status:
# - starting (initial period)
# - healthy (checks passing)
# - unhealthy (checks failing)
```

### Test Health Check Failure

```bash
# Stop MongoDB
docker compose stop mongodb

# Wait 30 seconds, then check API health
docker compose ps

# API health check will fail because it can't reach MongoDB
```

---

## Part 8: Debugging Common Issues

### Issue 1: Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Fix**:
```bash
# Find process using port
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yaml
ports:
  - "8001:8000"  # Host port 8001, container port 8000
```

### Issue 2: Container Keeps Restarting

**Fix**:
```bash
# Check logs
docker compose logs api

# Common causes:
# - Syntax error in code
# - Missing dependencies
# - Wrong environment variables
```

### Issue 3: Can't Connect to Database

**Fix**:
```bash
# Check if MongoDB is running
docker compose ps

# Check MongoDB logs
docker compose logs mongodb

# Verify connection string uses service name
# ✅ mongodb://mongodb:27017
# ❌ mongodb://localhost:27017
```

### Issue 4: Data Lost After Restart

**Fix**:
```bash
# Make sure volume is defined
# Check if volume exists
docker volume ls | grep mongo-data

# If missing, add to docker-compose.yaml:
volumes:
  mongo-data:
    driver: local
```

---

## Part 9: Practice Exercises

### Exercise 1: Add a New Endpoint

Add a `/reset` endpoint to your API that clears all visits:

```python
@app.delete("/reset")
def reset_visits():
    if not client:
        raise HTTPException(status_code=503, detail="Database not available")
    
    result = visits_collection.delete_many({})
    return {"deleted_count": result.deleted_count}
```

Test it:
```bash
curl -X DELETE http://localhost:8000/reset
curl http://localhost:8000/stats  # Should show 0 visits
```

### Exercise 2: Change MongoDB Password

1. Update password in `docker-compose.yaml`
2. Update `MONGODB_URL` in API service
3. Run `docker compose down -v` (removes old data)
4. Run `docker compose up --build`

### Exercise 3: Add Redis (Bonus)

Add Redis to your stack:

```yaml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

---

## Summary: Key Takeaways

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **docker-compose.yaml** | Multi-container definition | Run complex apps easily |
| **Services** | Named containers | Each service = one container |
| **Networks** | Container connectivity | Services talk via service names |
| **Volumes** | Persistent storage | Data survives container restarts |
| **Environment Variables** | Configuration | Change behavior without code changes |
| **Health Checks** | Container monitoring | Know when services are ready |
| **depends_on** | Startup order | Start database before API |

---

## Commands I Must Remember

```bash
docker compose up -d          # Start services in background
docker compose down           # Stop and remove containers
docker compose down -v        # Stop and remove volumes (data!)
docker compose logs -f        # Follow logs
docker compose ps             # Check service status
docker compose exec api sh    # Shell into container
docker compose restart api    # Restart one service
docker compose build          # Rebuild images
```

---

## Practice Checklist

- [ ] Started all services with `docker compose up`
- [ ] Tested all API endpoints (/, /health, /stats)
- [ ] Accessed Mongo Express UI
- [ ] Viewed logs for each service
- [ ] Tested data persistence (down + up)
- [ ] Practiced docker compose commands
- [ ] Understood networking (service names)
- [ ] Debugged at least one issue

---

**Completion Date**: ___________

**Time Spent**: ___________

**Confidence Level (1-10)**: ___________

**Questions**:
```
# Write down any questions or things to research
```
