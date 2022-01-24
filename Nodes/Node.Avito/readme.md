##Node Avito Parsing 

 Start 
```
 docker run -e=API_URL=adnotify_api -e=NAME='Node.Avito'  -e=API_KEY=token \
            -e HOUR_BEGIN=7 -e HOUR_END=23 -e PERIODIC_MINUTES=10 \
            --name adnotify.node.avito adnotify.node.avito;
 ```