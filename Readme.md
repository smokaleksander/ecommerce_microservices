
# Microservices sneakers e-commerce app

A brief description of what this project does and who it's for


## Tech Stack

**Client:** NextJS, Bootstrap

**Server:** Python, FastApi, MongoDB

**Infrastructure:** kubernetes

  
## Run Locally

Before run [Docker for desktop](https://www.docker.com/products/docker-desktop) and [Skaffold](https://skaffold.dev/) are required.

1. Clone the project

```bash
  git clone https://github.com/smokaleksander/ecommerce_microservices.git
```

2. Go to the project directory

```bash
  cd ecommerce_microservices
```

3. create [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/#docker-desktop )

```bash
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/cloud/deploy.yaml
```

4. create kubernetes secret with srtipe token 
```bash
  kubectl create secret generic stripe-secret --from-literal STRIPE_SECRET_KEY=your_key_here
```

5. Start the app

```bash
  skaffold dev
```

6. Go to [http://127.0.0.1](http://127.0.0.1)  

7. On "Privacy Error" screen type "thisisunsafe" and hit Enter
