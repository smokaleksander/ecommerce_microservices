import axios from 'axios';

const client = ({ req }) => {
    if (typeof window === 'undefined') {
        // call form server
        
        return axios.create({
                baseURL: 'https://ingress-nginx-controller.ingress-nginx.svc.cluster.local',
                headers: req.headers,
                rejectUnauthorized: false
        }); 
    } else {
        //call from browser
        return axios.create({
            baseURL: '/',
            rejectUnauthorized: false
        });
    }
};

export default client;