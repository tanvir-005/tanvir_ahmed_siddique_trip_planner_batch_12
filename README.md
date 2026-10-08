# Trip Planner
### Md Tanvir Ahmed Siddique - Inter Batch 12, W3 Engineers Ltd.

## Run the project (Beginner):
Just copy and paste the following command on your Linux Terminal
```
git clone https://github.com/tanvir-005/tanvir_ahmed_siddique_trip_planner_batch_12 && cd tanvir_ahmed_siddique_trip_planner_batch_12 && bash run.sh
```
## Run the Project (Advance):
1. Clone the reporsitory
2. Create Python Virtual Environment
3. Install the requirements
4. Create environment variables for address and port
5. Run run.py

## API Endpoints and Methods:
Route | Method
:---|:---
```/``` | ```GET``` 
```/health``` | ```GET``` 
```/api/v1/trips``` | ```GET``` 
```/api/v1/trips``` | ```POST``` 
```/api/v1/trips/<int:trip_id>``` | ```GET``` 
```/api/v1/trips/<int:trip_id>``` | ```PUT``` 
```/api/v1/trips/<int:trip_id>``` | ```DELETE``` 
```/api/v1/trips/<int:trip_id>/travelers``` | ```POST``` 
```/api/v1/trips/<int:trip_id>/expenses``` | ```POST``` 
```/api/v1/trips/<int:trip_id>/travelers/<int:traveler_id>``` | ```DELETE``` 
```/api/v1/trips/<int:trip_id>/summary``` | ```GET``` 
```/api/v1/trips/<int:trip_id>/status``` | ```PATCH``` 