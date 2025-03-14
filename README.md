## ASTRAL: Automated Safety Testing of LLMs 

ASTRAL automates the creation and execution of test cases (i.e., prompts) to evaluate LLM safety. It operates through three core modules: a test generator, a test executor, and a test evaluator. 
Integration options include a Docker image launching a REST API with interactive documentation, facilitating its use and integration. 
ASTRAL is part of the [Trust4AI](https://trust4ai.github.io/trust4ai/) research project.

## Index
1. [Usage](#usage)
2. [Repository structure](#repository-structure)
3. [Deployment](#deployment)
    1. [Installation](#installation)
    2. [Execution](#execution)
    3. [Docker](#docker)
4. [License and funding](#license-and-funding)

## Usage

To view the API documentation, access the following URL:

ASTRAL test generator:
```
http://localhost:5000/apidocs

```
ASTRAL tet executor:
```
http://localhost:5001/apidocs

```
ASTRAL test evaluator:
```
http://localhost:5003/apidocs

```


### Repository structure

This repository is structured as follows:

- `Dockerfile`: This file is a script containing a series of instructions and commands used to build a Docker image.
- `docker-compose.yml`: This YAML file allows you to configure application services, networks, and volumes in a
  single file, facilitating the orchestration of containers.
- `TestGenerator/swagger.yaml`: This file is used to describe the entire API of ASTRAL test generator, including available endpoints, operations on
  each endpoint, operation parameters, and the structure of the response objects. It's written in YAML format following
  the [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (OAS).
- `TestExecutor/swagger.yaml`: This file is used to describe the entire API of ASTRAL test executor, including available endpoints, operations on
  each endpoint, operation parameters, and the structure of the response objects. It's written in YAML format following
  the [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (OAS).
- `TestEvaluator/swagger.yaml`: This file is used to describe the entire API of ASTRAL test evaluator, including available endpoints, operations on
  each endpoint, operation parameters, and the structure of the response objects. It's written in YAML format following
  the [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) (OAS).
- `postman/`: This folder includes three collections of API requests (one for each ASTRAL service) saved in JSON format for use with Postman.
- `TestGenerator/`: This directory contains the source code for ASTRAL test generator.
- `TestExecutor/`: This directory contains the source code for ASTRAL test executor.
- `TestEvaluator/`: This directory contains the source code for ASTRAL test evaluator.
- `settings.py`: This file contains the OpenAI API key, Tavily (https://tavily.com/) API key, and Ollama server address.
- `requirements.txt`: This file lists the Python libraries required by the project.

## Deployment

### Installation

If you haven't downloaded the project yet, first clone the repository:

```bash
git clone https://github.com/Trust4AI/ASTRAL-REST-API.git
```

To install the project, run the following command:

```
pip install -r requirements.txt
```

### Settings

Specify the OpenAI API key, Tavily API key, and Ollama address in `settings.py`

### Execution

To run the ASTRAL test generator, execute the following command from the project directory:

```
python testGenerator_rest.py
```

This will run on port 5000. 

To run the ASTRAL test executor, execute the following command from the project directory:

```
python testExecutor_rest.py
```

This will run on port 5001. 

To run the ASTRAL test evaluator, execute the following command from the project directory:

```
python testEvaluator_rest.py
```

This will run on port 5002. 


### Docker


To run Docker Compose execute the following command:

```
docker-compose up -d
```


To stop the container, execute the following command:

```
docker-compose down
```

## License and funding

[Trust4AI](https://trust4ai.github.io/trust4ai/) is licensed under the terms of the GPL-3.0 license.

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not
necessarily reflect those of the European Union or European Commission. Neither the European Union nor the granting
authority can be held responsible for them. Funded within the framework of
the [NGI Search project](https://www.ngisearch.eu/) under grant agreement No 101069364.

<p align="center">
<img src="https://github.com/Trust4AI/trust4ai/blob/main/funding_logos/NGI_Search-rgb_Plan-de-travail-1-2048x410.png" width="350">
<img src="https://github.com/Trust4AI/trust4ai/blob/main/funding_logos/EU_funding_logo.png" width="250">
</p>

Actividad: C23.I1.P03.S01.01 ANDALUCÍA Subvención pública para el desarrollo del «Programa INVESTIGO», financiada con cargo a los fondos procedentes del «Mecanismo de Recuperación y Resiliencia».

<p align="center">
  <img src="https://github.com/Trust4AI/trust4ai/blob/main/funding_logos/Investigo.png" width="900">

</p>

