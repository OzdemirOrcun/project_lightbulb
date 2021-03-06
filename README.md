# lightbulb_project


Example Request for Turn On LightBulbs Manually 
POST REQUEST http://localhost:8010/lightbulb
{
    "status": "ok",
    "lamp": "1",
    "command":"on",
    "manuel": "1"
}



Example Request for Turn Off LightBulbs Manually 
POST REQUEST http://localhost:8010/lightbulb
{
    "status": "ok",
    "lamp": "1",
    "command":"off",
    "manuel": "1"
}



Example Request for Set Percentage of Brightness Manually
POST REQUEST http://localhost:8010/lightbulb
{
    "status": "ok",
    "lamp": "1",
    "command":"76",
    "manuel": "1"
}
