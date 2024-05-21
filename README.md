# BDL-Assignment7

## Instructions on how to run (all commands from root of directory) </br>

git clone </br>
pip install -r requirements.txt (after creating a virtual env) </br>

### Task 1 </br>
python api-app/fastapi-app.py api-app/bin/mnist-digitclassifier-model.keras </br>
./node_exporter --web.listen-address=:9200 & </br>
"Path To Prometheus Binary" --config.file=deploy/prometheus.yml </br>

### Task2 </br>
docker-compose up --build to build and run the image</br>

## Monitoring using Prometheus and Grafana</br>

Monitoring is an essential aspect of maintaining the reliability and performance of deployed applications. In the context of the FastAPI application, monitoring is implemented using Prometheus and Grafana. 

The FastAPI application exposes metrics using Prometheus, allowing for the collection and monitoring of various performance indicators. The following are monitored as required.

**api_call_counter** : Counter for tracking the API usage from different client IP addresses. </br>
**api_len_input** : Gauge for length of input </br>
**api_runtime_secs** : Gauge for total time taken of the API </br>
**api_TL_ratio** : Gauge for T/L time or effective processing time (in micro-sec per character)  </br>

### Node Exporter 

In addition to monitoring application-specific metrics, the monitoring setup may include Node Exporter. Node Exporter is a Prometheus exporter for system metrics, providing insights into the underlying infrastructure’s health and resource utilization. It collects metrics such as CPU usage, memory usage, disk I/O, and network activity from the host system. 

### Some sample visualizations from grafana 
![Screenshot from 2024-05-21 09-51-14](https://github.com/dhan-02/BDL-Assignment7/assets/74642765/36cc1f75-ca5f-4c8d-a20b-66a0647985fb)
![Screenshot from 2024-05-21 09-58-11](https://github.com/dhan-02/BDL-Assignment7/assets/74642765/31e42b48-b674-4e74-9560-645cd5c41ba6)
![Screenshot from 2024-05-21 09-59-57](https://github.com/dhan-02/BDL-Assignment7/assets/74642765/2776029e-2154-4fa9-aeb4-5597efeb5b49)

## Dockerization

Since, we want to dockerize the app with monitoring, we write two separate docker files, one each for the the fast-api-app and the other for prometheus. We then use a docker compose command to run these containers simultaneously. One issue with this is the fact that docker compose is different from docker run in terms of how we give flags for cpu usage and port mapping. The docker compose file is shown below 
![Screenshot from 2024-05-21 09-29-19](https://github.com/dhan-02/BDL-Assignment7/assets/74642765/52eb4fe8-03b0-4932-ab70-dac031db772e)
