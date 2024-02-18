<h1 align="center">Webhook plugin for SpaceONE</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://user-images.githubusercontent.com/35549653/76694897-de236300-66bb-11ea-9ace-b9edde9c12da.png">  
  <p> 
   <br>
    <img  alt="Version"  src="https://img.shields.io/badge/version-1.1-blue.svg?cacheSeconds=2592000"  />    
    <a  href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank">  
        <img  alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg"  />  
    </a> 
    </p> 
</div>    



> SpaceONE's [plugin-api-direct-mon-webhook](https://github.com/spaceone-dev/plugin-api-direct-mon-webhook) 
 is a tool that can integrate and manage events of from 3rd-party system.   
> SpaceONE already supports various external monitoring ecosystems in the form of plug-ins   
> If you want to integrate SpaceONE with the monitoring system you are operated, deliver the events to this plugin webhook.

Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/plugin-api-direct-mon-webhook)
> Latest stable version : 1.2.4

Please contact us if you need any further information. (support@spaceone.dev)

---

## Body of the request

```json
{
    "options": {},
    "data": {
        "event_key": "xa339sa9b09sd94jgx1234vlkajdflk",
        "event_type": "ALERT",
        "title": "This is test event",
        "description": "This is Sample Event. It's sample description.",
        "severity": "ERROR",
        "rule": "this is event rule",
        "image_url": "https://sample.io/img/sdfsdf",
        "provider": "aws",
        "account": "aws-account-id",
        "resource": {
            "resource_id": "resource-xzasdfasdf",
            "resource_type": "server",
            "name": "resource_name"
        },
        "additional_info": {
            "asdlkafjsdlkf": "asdfasdf"
        },
        "occurred_at": "datetime"
    }
}
```

| **Parameter**            | **Description**      | **Examples**  |
|--------------------------| -------------------- | ------------- | 
| `event_key`              | event unique key     | |
| `event_type`             | Type of event.       | `RECOVERY`, `ALERT`, `ERROR` |
| `title`                  | Title of event       | |
| `description`            | Description of event | |
| `severity`               | Severity of event    | `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `NOT_AVAILABLE` |
| `rule`                   | Rule in which the event was triggered                  | |
| `image_url`              | URL include the image associated with the event        | |
| `provider`               | Provider of the resource which the event was generated | |
| `account`                | Account ID of the resource which the event was generated| |
| `resource.resource_id`   | ID of the resource which the event was generated       | |
| `resource.resource_type` | The type of the resource which the event was generated | |
| `resource.name`          | Name of resource | |
| `additional_info`        | Additional information about the event. It is a dictionary type, and both key and value must be string type.| |
| `occurred_at`            | Time when the event occurred. | |
---

## Supported options
### load_json
Load the json in the body of the request.
Example:
```json
{
    "options": {
        "load_json": [
            "Message",
            "AdditionalInfo"
        ]
    }
}
```

### convert_data
Convert the body of the request using the jinja2 template.
Example:
```json
{
    "options": {
        "convert_data": {
           "event_key": "{{ Message.id }}",
           "title": "{{ Message.detail.EventID }}",
           "account": "{{ Message.account }}",
           "resource": {
               "resource_id": "{{ Message.detail.SourceArn }}"
           },
           "occurred_at": "{{ Message.detail.Date }}"
       }
    }
}
```

## Release note

### Ver 1.2.4
Enhancement
- Add option to load json in the body of the request
- Add option to convert the body of the request using the jinja2 template

### Ver 1.1

Enhancement
- Add validation in API Direct Webhook [#7](https://github.com/spaceone-dev/plugin-api-direct-mon-webhook/issues/7)
