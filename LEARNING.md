# DevOps Learning Log

Track everything I learn throughout the 12-month journey.

---

## Week 0-2: Docker Fundamentals

### Concepts Learned
- **Dockerfile**: Recipe/instructions to build an image
- **Image**: Frozen package (app + dependencies), immutable
- **Container**: Running instance of an image
- **Registry**: Cloud storage for images (like GitHub for code)
  - GitHub Container Registry (GHCR): `ghcr.io`
  - Docker Hub: `docker.io`

### Commands Mastered
```bash
# Docker Build & Run
docker build -t simple-api:local .           # Build image from Dockerfile
docker run --rm -p 8000:8000 simple-api:local  # Run container (--rm = auto-delete when stopped)
docker ps                                     # List running containers
docker images                                 # List images on system

# Docker Registry
docker login ghcr.io -u USERNAME              # Authenticate to registry
docker tag simple-api:local ghcr.io/user/simple-api:latest  # Create alias/tag
docker push ghcr.io/user/simple-api:latest    # Upload to registry
docker pull ghcr.io/user/simple-api:latest    # Download from registry

# Testing
curl http://localhost:8000/health             # Test API endpoint
```

### Files I Created
- `simple-api/Dockerfile` - Instructions to build Python FastAPI container
- `simple-api/.dockerignore` - Files to exclude from image
- `.gitignore` - Files to exclude from Git

### Key Insights
- Use slim base images (`python:3.12-slim`) to reduce size
- Copy `requirements.txt` first for better layer caching
- `EXPOSE` documents ports but doesn't actually publish them
- `--rm` flag cleans up containers automatically

### Apple Silicon (M4 Pro) Notes
- Default builds are `linux/arm64` architecture
- Most modern images support arm64
- Use `--platform linux/amd64` if needed for compatibility

---

## Week 1: Linux Operator Basics

### Concepts Learned
- **systemd**: Modern Linux init system and service manager
- **File Permissions**: rwx (read/write/execute) for owner/group/others
- **Process Management**: Understanding PID, process states (R/S/Z/D)
- **System Logs**: journalctl for systemd logs, traditional /var/log files
- **Networking**: TCP/UDP ports, listening services, DNS resolution

### Commands Mastered
```bash
# System Information
whoami                        # Current user
uname -a                      # System info
df -h                         # Disk usage
free -h                       # Memory usage
lscpu                         # CPU info

# File & Permissions
ls -lah                       # List files with details
chmod 755 file                # Change permissions (rwxr-xr-x)
chown user:group file         # Change ownership

# Networking
ip addr show                  # Show IP addresses
ss -tuln                      # List listening ports
ping -c 4 host                # Test connectivity
dig domain.com                # DNS lookup
curl URL                      # Test HTTP endpoints
nc -zv host port              # Check if port is open

# Process Management
ps aux                        # List all processes
top / htop                    # Interactive process viewer
kill PID                      # Terminate process gracefully
kill -9 PID                   # Force kill process
systemctl status service      # Check service status
systemctl start/stop service  # Control services

# Logs & Debugging
journalctl -n 50              # Last 50 log lines
journalctl -u service         # Logs for specific service
journalctl -f                 # Follow logs in real-time
tail -f /var/log/syslog       # Follow traditional log file

# Text Processing
grep "pattern" file           # Search in file
wc -l file                    # Count lines
head/tail file                # First/last lines
cat file                      # Show content
less file                     # Page through content
```

### Practice Environment
- **Tool**: Lima (Linux VM on macOS)
- **Distribution**: Ubuntu 25.10 (arm64)
- **Commands**: `limactl shell devops-lab` to connect

### Key Insights
- Always check logs first when debugging (journalctl)
- `ss -tuln` shows what's listening on which ports
- File permissions: r=4, w=2, x=1 (755 = rwxr-xr-x)
- Process states: R=Running, S=Sleeping, Z=Zombie
- Use `systemctl status` before checking logs

### Troubleshooting Checklist
1. Is the service running? (`systemctl status`)
2. What do the logs say? (`journalctl -u service`)
3. Is the port open? (`ss -tuln`)
4. Can I connect locally? (`curl localhost:port`)
5. Firewall blocking? (`sudo ufw status`)

---

## Week 3: [Next Topic]

_To be added..._

---

## Common Errors & Fixes

### "Cannot connect to Docker daemon"
**Fix**: Start Docker Desktop, wait for whale icon to be steady

### "Port already in use"
**Fix**: 
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

### "docker command not found"
**Fix**: Docker Desktop not installed or not in PATH

---

## Resources Used
- Docker in 100 Seconds (video)
- FastAPI docs
- GitHub Container Registry docs

---

## Questions to Research Later
- [ ] How to do multi-stage Docker builds
- [ ] Difference between CMD and ENTRYPOINT
- [ ] Docker volumes for persistent data
- [ ] Docker networking modes
