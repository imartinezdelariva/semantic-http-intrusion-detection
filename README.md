# Detection of Cybersecurity Attacks in Local Networks Using Embeddings and Semantic Analysis

Bachelor's Thesis in Telecommunication Technologies Engineering at Universidad Pontificia Comillas (ICAI).

This project explores whether HTTP network traffic can be treated as natural-language text and classified according to its semantic meaning. The resulting intrusion detection system uses language embeddings and vector similarity to distinguish normal traffic from four categories of web attack.

## Overview

The complete experimental dataset was generated in a controlled local network built with GNS3 and VirtualBox. HTTP traffic was sent to a deliberately vulnerable DVWA server, captured as PCAP files and processed in Python.

Each HTTP request-response pair was transformed into a 1,536-dimensional vector using OpenAI's `text-embedding-3-small` model. The vectors were stored in Elasticsearch and new samples were classified using K-Nearest Neighbours with `k=1` and cosine similarity.

The final system achieved an overall mean accuracy of **88.3%** using an index containing **1,208 training documents** and an independent evaluation set of **693 samples**.

## Traffic categories

The attack categories were selected from common web application security risks covered by OWASP guidance. SQL Injection and Command Injection belong to the broader Injection category, XSS is one of the most widespread web application attacks, and Brute Force is related to authentication failures.

- Normal HTTP traffic
- SQL Injection (SQLI)
- Cross-Site Scripting (XSS)
- Brute Force
- Command Injection

Each category was generated at the Low, Medium and High DVWA difficulty levels.

## System pipeline

1. Generate normal and malicious HTTP traffic against DVWA.
2. Capture the traffic with `tcpdump` at the network router.
3. Read and filter the PCAP files using Scapy.
4. Group packets into HTTP request-response pairs.
5. Convert each pair into a semantic embedding.
6. Store labelled vectors in Elasticsearch.
7. Classify evaluation samples through KNN vector search.
8. Analyse accuracy, confusion matrices, URL dependence and cosine scores.

## Experimental environment

The network laboratory contained three VirtualBox machines connected through GNS3:

| Node | Address | Role |
| --- | --- | --- |
| PC1 | `192.168.10.10` | Traffic generator |
| Router | `192.168.10.1 / 192.168.20.1` | Routing and traffic capture |
| PC2 | `192.168.20.10` | DVWA server |

DVWA (Damn Vulnerable Web Application) is an intentionally insecure PHP/MySQL web application designed for cybersecurity education and controlled security testing. It implements real web vulnerabilities and provides three security levels - Low, Medium and High - which change the protections applied by the server and therefore the complexity and structure of the generated traffic.

For this project, DVWA ran inside a Docker container on PC2 and acted as the target application for both normal requests and controlled attacks. Its SQL Injection, reflected XSS, Brute Force and Command Injection modules made it possible to generate real HTTP request-response exchanges for every category and difficulty level. This was important because the system was evaluated with traffic captured from a functioning application rather than with manually written log entries.

Caddy acted as a reverse proxy between the traffic generator and the DVWA container. The router captured the unencrypted laboratory HTTP traffic with `tcpdump`, and Samba was used to transfer the resulting PCAP files to the analysis machine.

All attacks were executed exclusively against the deliberately vulnerable application in this isolated and authorised environment.

## Dataset generation

Thirty Python scripts were developed to automate traffic generation:

- 15 scripts for training data
- 15 scripts for evaluation data
- Separate scripts for every traffic category and difficulty level

The training and evaluation scripts used different payload sets. Each PCAP file contained only one category, one difficulty level and one experimental purpose, preserving independence between the two datasets.

## Results

### Final classification accuracy

| Traffic category | Low | Medium | High | Mean |
| --- | ---: | ---: | ---: | ---: |
| Normal | 84.2% | 71.0% | 83.8% | 79.7% |
| XSS | 88.2% | 93.9% | 94.1% | 92.1% |
| SQLI | 90.9% | 93.6% | 72.2% | 85.6% |
| Brute Force | 88.2% | 88.2% | 100.0% | 92.1% |
| Command Injection | 89.8% | 91.7% | 93.8% | 91.8% |
| **Overall mean** | **88.3%** | **87.7%** | **88.8%** | **88.3%** |

### URL ablation experiment

DVWA includes the attack name in some URL paths, which could provide an artificial classification signal. To measure this effect, three configurations were evaluated:

- **C1:** real URLs during training and evaluation
- **C2:** real training URLs and randomised evaluation URLs
- **C3:** randomised URLs during both training and evaluation

XSS and Command Injection remained stable when the paths were randomised, indicating that their classification relied primarily on payload semantics. SQLI recovered when training and evaluation used consistent randomised paths. Brute Force remained the most dependent on the URL because its credentials are semantically similar to normal login traffic.

### Confidence analysis

Cosine similarity scores were also evaluated as potential confidence indicators. Since the embeddings contain 1,536 dimensions, most scores were concentrated between approximately `0.979` and `0.999`.

The experiments showed that a high cosine score is not a universally reliable indication of a correct prediction. In some categories, incorrectly classified samples were assigned higher scores than correct predictions.

## Main limitations

- The experiments used a controlled DVWA environment rather than production network traffic.
- The system analyses HTTP content but not temporal or behavioural patterns, limiting the detection of attacks such as time-based blind SQL Injection and Brute Force.
- The study covers four attack categories, so additional traffic sources and attack types are required before considering operational use.

## Technologies

- Python and Jupyter Notebook
- GNS3 and VirtualBox
- Scapy, tcpdump and Wireshark
- Docker, DVWA and Caddy
- Elasticsearch
- OpenAI Embeddings API
- NumPy, pandas, Matplotlib and Seaborn

## Future work

- Validate the system using traffic from environments other than DVWA
- Expand the dataset and the number of attack categories
- Add temporal and behavioural network features
- Build an LLM-assisted forensic analysis interface
- Investigate real-time detection and automated response

## Author

**Iñigo Martínez de la Riva Muinelo**  
Universidad Pontificia Comillas - ICAI  
Academic year 2025-2026

## Disclaimer

This repository is intended exclusively for academic research and cybersecurity education. The attack-generation scripts must only be used in systems where explicit authorisation has been granted.
