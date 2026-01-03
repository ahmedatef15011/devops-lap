# Week 1: Linux Operator Basics

**Goal**: Master the essential Linux commands and debugging tools used daily in DevOps.

**VM Details**:
- Distribution: Ubuntu 25.10 (arm64)
- Tool: Lima
- Access: `limactl shell devops-lab`

---

## Part 1: System Information & Navigation

### Basic Info Commands

Connect to your VM first:
```bash
limactl shell devops-lab
```

Then run these commands and document the output:

```bash
# Who am I?
whoami

# What system am I on?
uname -a

# OS details
cat /etc/os-release

# Current directory
pwd

# List files (long format, human readable)
ls -lah

# Disk usage
df -h

# Memory info
free -h
```

**My Notes**:
```
I am using ubuntu linux
338Mi used out of 1.9Gi from memory
```

---

## Part 2: Users & Permissions

### Understanding Users

```bash
# Current user info
id

# List all users
cat /etc/passwd | tail -5

# Check sudo access
sudo -l
```

### File Permissions Practice

```bash
# Create a test directory
mkdir -p ~/devops-practice
cd ~/devops-practice

# Create a test file
echo "Hello DevOps" > test.txt

# Check permissions
ls -l test.txt

# Understanding: -rw-r--r--
# - = file (d = directory)
# rw- = owner can read/write
# r-- = group can read
# r-- = others can read

# Change permissions (make executable)
chmod +x test.txt
ls -l test.txt

# Change ownership (you'll need sudo)
sudo chown root:root test.txt
ls -l test.txt

# Change back
sudo chown $(whoami):$(whoami) test.txt
```

**My Notes**:
```
# What permissions mean:
# r (read) = 4
# w (write) = 2
# x (execute) = 1
# Example: chmod 755 = rwxr-xr-x
```

---

## Part 3: Networking & Debugging

### Essential Network Commands

```bash
# Check IP address
ip addr show

# Alternative (simpler)
hostname -I

# Check listening ports
ss -tuln
# t = TCP, u = UDP, l = listening, n = numeric (don't resolve names)

# Test connectivity
ping -c 4 google.com

# DNS lookup
dig google.com

# Simpler DNS
nslookup google.com

# Check if port is open (test external service)
nc -zv google.com 443
```

### Test Your API from the VM

```bash
# Your Mac's IP (from Mac terminal, not VM)
# Run on Mac: ipconfig getifaddr en0

# From VM, test your Mac's API
curl http://YOUR_MAC_IP:8000/health

# Or test a public API
curl -i https://api.github.com/users/ahmedatef15011
# -i = include HTTP headers
```

**My Notes**:
```
# Common ports to remember:
# 22 = SSH
# 80 = HTTP
# 443 = HTTPS
# 3306 = MySQL
# 5432 = PostgreSQL
# 6379 = Redis
```

---

## Part 4: Process & System Monitoring

### Process Management

```bash
# List all processes
ps aux

# Interactive process viewer
top
# Press 'q' to quit

# Better version (install first)
sudo apt update && sudo apt install -y htop
htop

# Find specific process
ps aux | grep ssh

# Check system load
uptime

# Check CPU info
lscpu

# Check running services
systemctl list-units --type=service --state=running
```

### Kill a Process (Practice)

```bash
# Start a dummy process in background
sleep 3600 &

# Find its PID
ps aux | grep sleep

# Kill it gracefully
kill <PID>

# Force kill (if needed)
# kill -9 <PID>
```

**My Notes**:
```
# Process states:
# R = Running
# S = Sleeping
# Z = Zombie (dead but not cleaned up)
# D = Uninterruptible sleep (usually I/O)
```

---

## Part 5: Logs & Troubleshooting

### System Logs

```bash
# View system logs (systemd journal)
sudo journalctl -n 50
# -n 50 = last 50 lines

# Follow logs in real-time
sudo journalctl -f
# Press Ctrl+C to stop

# Logs for specific service
sudo journalctl -u ssh -n 20

# Boot logs
sudo journalctl -b

# Errors only
sudo journalctl -p err

# Traditional log files
ls -lh /var/log/
tail -20 /var/log/syslog
```

### Debugging Practice

```bash
# Install nginx for testing
sudo apt update
sudo apt install -y nginx

# Check if it started
systemctl status nginx

# Check which port it's using
sudo ss -tuln | grep 80

# Check nginx logs
sudo tail -f /var/log/nginx/access.log

# Stop it
sudo systemctl stop nginx

# Check status again
systemctl status nginx
```

**My Notes**:
```
# Troubleshooting checklist:
# 1. Is the service running? (systemctl status)
# 2. What do the logs say? (journalctl)
# 3. Is the port open? (ss -tuln)
# 4. Can I connect locally? (curl localhost)
# 5. Firewall blocking? (sudo ufw status)
```

---

## Part 6: Useful Tools & Tricks

### Text Processing

```bash
# Search in files
grep "error" /var/log/syslog

# Count lines
wc -l /etc/passwd

# Show file content
cat /etc/hosts

# Page through content
less /var/log/syslog

# First 10 lines
head /etc/passwd

# Last 10 lines
tail /etc/passwd

# Find files
find /var/log -name "*.log"

# Disk usage by directory
du -sh /var/log/*
```

### Piping & Redirection

```bash
# Pipe output to another command
ps aux | grep nginx

# Save to file
ps aux > processes.txt

# Append to file
echo "new line" >> processes.txt

# Redirect errors
ls /nonexistent 2> errors.txt

# Redirect both stdout and stderr
ls /nonexistent &> all_output.txt
```

**My Notes**:
```
# Pipe operators:
# | = send output to next command
# > = write to file (overwrite)
# >> = append to file
# 2> = redirect errors
# &> = redirect everything
```

---

## Common Scenarios & Solutions

### Scenario 1: Service Won't Start

```bash
# Check status
systemctl status service-name

# Check logs
journalctl -u service-name -n 50

# Check if port is already in use
ss -tuln | grep PORT_NUMBER
```

### Scenario 2: Disk Full

```bash
# Check disk space
df -h

# Find large files
du -h /var | sort -hr | head -20

# Clean up (be careful!)
sudo apt clean
```

### Scenario 3: Can't Connect to Service

```bash
# Test locally first
curl localhost:PORT

# Check if service is listening
ss -tuln | grep PORT

# Check firewall
sudo ufw status

# Check from another machine
telnet IP PORT
```

---

## Summary: Commands I Must Remember

| Command | What It Does | When To Use |
|---------|--------------|-------------|
| `systemctl status SERVICE` | Check service status | Debugging services |
| `journalctl -u SERVICE` | View service logs | Finding errors |
| `ss -tuln` | List listening ports | Check what's running |
| `curl URL` | Test HTTP endpoints | Verify API works |
| `ps aux \| grep NAME` | Find process | Before killing |
| `df -h` | Disk space | Check capacity |
| `free -h` | Memory usage | Performance issues |
| `top` / `htop` | Monitor system | See resource usage |

---

## Practice Exercises Completed

- [x] Connected to VM successfully
- [x] Ran all commands in Part 1-6
- [x] Installed and tested nginx
- [x] Practiced grep, tail, journalctl
- [x] Killed a process safely
- [x] Understood file permissions

---

**Completion Date**: January 2, 2026

**Time Spent**: ~3-4 hours

**Confidence Level (1-10)**: 8

---
