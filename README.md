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

### Results

Here are some test runs of using the v4d object:

- 100x100x100x100 | random frames w/ 95% transparency | 2m 22s | 660MB compressed | 760MB uncompressed | M1 MAX 10 Core
- 100x100x100x100 | still frames w/ 95% transparency | 2m 22s | 3.6MB compressed | 7.6MB uncompressed | M1 MAX 10 Core
- 1000x100x100x100 | still frames w/ 95% transparency | 24m 38s | 36.9MB compressed | 76MB uncompressed | M1 MAX 10 Core
