# Nginx customization

This customization is working with nginx ingress controller. There is only basic setup to get this running.


## Running In Minikube

To run midpoint live demo in minikube, you need following.

***Assumption***:
we're running command  `./midpoint-live-demo-setup.sh -a example.com`


- install `minikube`
- run `minikube addons enable ingress`
- go to root folder of `midpoint-live-demo`
- run `./midpoint-live-demo-setup.sh`

    - there are several options in this:
        | Option | Description |
        | ------ | ----------- | 
        | -n | Namespace where to deploy demo [default to mp-demo] |
        | -o | path to overlay, eg   overlays/nginx [default to overlays/nginx] |
        | -c | path to ingress certificates [default generated] | 
        | -a | domain for ingresses, [default to example.com] |
        | -i | custom ingressClass name [ingress class from annotation] |
        | -t | run minikube tunnel, after deployment [default to false] |
    - if you change the domain (-a) the new domain will be used even for the services bellow.

- if you use -t argument, `sudo minikube tunnel` will be started and you will be prompted for password
  - otherwise you need to run `sudo minikube tunnel` by your own
  - Ingresses are exposed as follows:
    | Application | Path |
    | ------ | ----------- | 
    | library | library.example.com |
    | fake-smtp | mail.example.com |
    | keycloak | kc.example.com |
    | midpoint | midpoint.example.com |
    | odoo | odoo.example.com |
    | ldap | ldap.example.com |
    | addressbook | addressbook.example.com |
    | hr | hr.example.com |
- you need to edit /etc/hosts files to be able to redirect to desired ingresses (add following)
```
127.0.0.1       kc.example.com
127.0.0.1       library.example.com
127.0.0.1       mail.example.com
127.0.0.1       midpoint.example.com
127.0.0.1       odoo.example.com
127.0.0.1       ldap.example.com
127.0.0.1       addressbook.example.com
127.0.0.1       hr.example.com
```

- now you should be able to go to browser and enter eg. `odoo.example.com` to visit odoo mainpage