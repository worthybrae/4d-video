# 4D Video

![Visualization](/assets/example.png)

### Getting Started

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Overview

This repo contains scripts that generate 3d videos. Each "video" is composed of a sequential series of 3d matrices containing rgba values. Different scripts explore optimization concepts like:

- using sparse matrices to optimize file size and performance
- storing differential changes from the inital frame to optimize file size and performance
- using compression techniques to optimize file size
