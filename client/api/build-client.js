import axios from 'axios';

export default ({ req }) => {
    if (typeof window === 'undefined') {
        // call form server
        
        return axios.create({
                baseURL: 'http://ingress-nginx-controller.ingress-nginx.svc.cluster.local',
                headers: req.headers
        }); 
    } else {
        //call from browser
        return axios.create();
    }
};