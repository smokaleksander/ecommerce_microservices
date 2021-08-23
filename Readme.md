
first run:
install  ingress-nginx
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.44.0/deploy/static/provider/cloud/deploy.yaml
edit /etc/hosts 
    add 127.0.0.1 'domain_name'

Create k8s secret with srtipe key
kubectl create secret generic stripe-secret --from-literal STRIPE_SECRET_KEY=your_key_here

skaffold dev
ecom.dev
if privacy error -> type 'thisisunsafe'

sec run:
run in docker-desktop k8s ns 'ecom'
skaffold dev