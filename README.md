# Sensor Node API

** note: Given the scope of this take-home assessment, I focused on delivering a solid foundation that meets the requirements. If this were a production setting, I would further enhance it by adding better error handling and exception management, more thorough documentation, additional unit tests, and database versioning to ensure maintainability and scalability.


### Future Improvements (if this were production)
- setting up postgres database with indexing
- database versioning (using alembic)
- docker container to run using WSGI
- CI/CD with github actions to allow multiple environments hosted
- end-to-end testing (using postman)

## API Documentation v1.0
## Quick Links
- [Deployment](#deployment)
  - [Docker Deployment](#docker-deployment)
  - [Local Development](#local-development)
- [Nodes Endpoints](#nodes-endpoints)
- [Sensors Endpoints](#sensors-endpoints)
- [Health Check Endpoint](#health-check-endpoint)
- [Response Codes](#response-codes)
- [Future Improvements](#future-improvements)

### Deployment

#### Docker Deployment
1. Build and start the containers:
```bash
docker-compose up --build -d
```

2. Run tests in Docker:
```bash
docker-compose run test
```

3. Stop and remove containers:
```bash
docker-compose down
```

#### Local Development
1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export FLASK_APP=src.app:application
export FLASK_ENV=development
```

4. Run the application:
```bash
flask run --host=0.0.0.0 --port=8000
```

5. Run tests locally:
```bash
python -m unittest discover tests -v
```

6. Run specific test file:
```bash
python -m unittest tests/test_sensors.py -v
```

Access the API at:
- Docker: `http://localhost:5000`
- Local: `http://localhost:8000`

### Nodes Endpoints

#### 1. Get All Nodes
- **Endpoint:** `/api/nodes`
- **HTTP Method:** GET
- **Path Parameters:** `firmware_version` (optional) 
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "serial_number": "NODE123",
      "firmware_version": "1.0.0",
      "sensors": []
    }
  ]
  ```
- **Description:** Retrieves all nodes in the system

#### 2. Get Single Node
- **Endpoint:** `/api/nodes/<identifier>`
- **HTTP Method:** GET
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "NODE123",
    "firmware_version": "1.0.0",
    "sensors": [
      {
        "id": 1,
        "serial_number": "SENSOR1",
        "manufacturer": "Test Mfg",
        "model": "MODEL-A",
        "modality": "Temperature",
        "node_id": 1
      }
    ]
  }
  ```
- **Description:** Retrieves a specific node and its associated sensors

#### 3. Create Node
- **Endpoint:** `/api/nodes`
- **HTTP Method:** POST
- **Request Body:**
  ```json
  {
    "serial_number": "NODE123",
    "firmware_version": "1.0.0"
  }
  ```
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "NODE123",
    "firmware_version": "1.0.0",
    "sensors": []
  }
  ```
- **Description:** Creates a new node

#### 4. Update Node
- **Endpoint:** `/api/nodes/<identifier>`
- **HTTP Method:** PUT
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Request Body:**
  ```json
  {
    "firmware_version": "2.0.0"
  }
  ```
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "NODE123",
    "firmware_version": "2.0.0",
    "sensors": []
  }
  ```
- **Description:** Updates an existing node's attributes

#### 5. Delete Node
- **Endpoint:** `/api/nodes/<identifier>`
- **HTTP Method:** DELETE
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Response:** 204 No Content
- **Description:** Deletes a node and its associated sensors

#### 6. Connect Sensor to Node
- **Endpoint:** `/api/nodes/<node_identifier>/sensors/<sensor_identifier>`
- **HTTP Method:** POST
- **Path Parameters:** 
  - `node_identifier` (required, ID or serial number)
  - `sensor_identifier` (required, ID or serial number)
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "SENSOR1",
    "manufacturer": "Test Mfg",
    "model": "MODEL-A",
    "modality": "Temperature",
    "node_id": 2
  }
  ```
- **Description:** Connects an existing sensor to a node
- **Error Responses:**
  ```json
  {
    "error": "Node not found"
  }
  ```
  ```json
  {
    "error": "Sensor not found"
  }
  ```
  
### Sensors Endpoints

#### 1. Get All Sensors
- **Endpoint:** `/api/sensors`
- **HTTP Method:** GET
- **Path Parameters:** `manufacturer` (optional), `model` (optional), `modality` (optional)
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "serial_number": "SENSOR1",
      "manufacturer": "Test Mfg",
      "model": "MODEL-A",
      "modality": "Temperature",
      "node_id": 1
    }
  ]
  ```
- **Description:** Retrieves all sensors in the system

#### 2. Get Single Sensor
- **Endpoint:** `/api/sensors/<identifier>`
- **HTTP Method:** GET
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "SENSOR1",
    "manufacturer": "Test Mfg",
    "model": "MODEL-A",
    "modality": "Temperature",
    "node_id": 1
  }
  ```
- **Description:** Retrieves a specific sensor

#### 3. Create Sensor
- **Endpoint:** `/api/sensors`
- **HTTP Method:** POST
- **Request Body:**
  ```json
  {
    "serial_number": "SENSOR1",
    "manufacturer": "Test Mfg",
    "model": "MODEL-A",
    "modality": "TEMPERATURE",
    "node_id": 1
  }
  ```
- **Valid Modality Types:**
  - `TEMPERATURE`
  - `WIND`
  - `HUMIDITY`
  - `PRESSURE`
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "SENSOR1",
    "manufacturer": "Test Mfg",
    "model": "MODEL-A",
    "modality": "Temperature",
    "node_id": 1
  }
  ```
- **Description:** Creates a new sensor

#### 4. Update Sensor
- **Endpoint:** `/api/sensors/<identifier>`
- **HTTP Method:** PUT
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Request Body:**
  ```json
  {
    "modality": "HUMIDITY",
    "model": "MODEL-B"
  }
  ```
- **Response Example:**
  ```json
  {
    "id": 1,
    "serial_number": "SENSOR1",
    "manufacturer": "Test Mfg",
    "model": "MODEL-B",
    "modality": "Humidity",
    "node_id": 1
  }
  ```
- **Description:** Updates an existing sensor's attributes

#### 5. Delete Sensor
- **Endpoint:** `/api/sensors/<identifier>`
- **HTTP Method:** DELETE
- **Path Parameters:** `identifier` (required, ID or serial number)
- **Response:** 204 No Content
- **Description:** Deletes a sensor

### Health Check Endpoint

#### 1. Health Check
- **Endpoint:** `/api/health`
- **HTTP Method:** GET
- **Response Example:**
  ```json
  {
    "status": "healthy"
  }
  ```
- **Description:** Checks API health status

### Response Codes
- **200:** Success
- **201:** Created
- **204:** Deleted
- **400:** Bad Request
- **404:** Not Found
- **500:** Server Error

