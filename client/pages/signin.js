import {useState} from 'react';
import Router from 'next/router';
//import axios from 'axios';
import useRequest from '../hooks/use-request';

export default () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    const {doRequest, errors } = useRequest({
        url: '/api/users/signin',
       
        method: 'post',
        body: params,
        onSuccess: () => Router.push('/')

    });

    const onSubmit = async (event) => {
        event.preventDefault();

        doRequest();
    };
    return (
        <form onSubmit={onSubmit}>
            <h1>Sign In</h1>
            <div className='form-group'>
                <label>Email Address</label>
                <input 
                    className='form-control'
                    value={email} 
                    onChange={e => setEmail(e.target.value)}
                />
            </div>
            <div className='form-group'>
                <label>Password</label>
                <input 
                    type='password' 
                    className='form-control'
                    value={password} 
                    onChange={e => setPassword(e.target.value)}
                />
            </div>

            
            {errors}
                    
            <button className='btn btn-primary'>Sign In</button>
        </form>
    );
};