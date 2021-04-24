import {useState} from 'react';
import Router from 'next/router';
import useRequest from '../hooks/use-request';

export default () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password_repeat, setPasswordRepeat] = useState('');
    const [fullname, setFullname] = useState('');
    const {doRequest, errors } = useRequest({
        url: '/api/users/signup',
        method: 'post',
        body: {
            fullname, 'username':email, password, password_repeat
        },
        onSuccess: () => Router.push('/')

    });

    const onSubmit = async (event) => {
        event.preventDefault();

        doRequest();
    };
    return (
        <form onSubmit={onSubmit}>
            <h1>Sign Up</h1>
            <div className='form-group'>
                <label>Fullname</label>
                <input 
                    className='form-control'
                    value={fullname} 
                    onChange={e => setFullname(e.target.value)}
                />
            </div>
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
            <div className='form-group'>
                <label>Repeat password</label>
                <input 
                    type='password' 
                    className='form-control'
                    value={password_repeat} 
                    onChange={e => setPasswordRepeat(e.target.value)}
                />
            </div>
            
            {errors}
                    
            <button className='btn btn-primary'>Sign Up</button>
        </form>
    );
};