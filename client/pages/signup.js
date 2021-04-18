import {useState} from 'react';
import axios from 'axios';

export default () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [password_repeat, setPasswordRepeat] = useState('');
    const [fullname, setFullname] = useState('');
    const [errors, setErrors] = useState([]);

    const onSubmit = async (event) => {
        event.preventDefault();

        try {
            
            const response = await axios.post('api/users/signup', {
            username, fullname, email, password, password_repeat, 
            });
            console.log(response);
            
        } catch (err) {
            setErrors(err.response.data.errors);
        }
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
                <label>Username</label>
                <input 
                    className='form-control' 
                    alue={username} 
                    onChange={e => setUsername(e.target.value)}
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
            
            <div className='alert-danger'>
                <h4>There is something you need to check</h4>
                <ul className='my-0'>
                    {errors.map(err => (
                        <li key={err.message}>{err.msg}</li>
                    ))}
                </ul>
            </div>
                    
            <button className='btn btn-primary'>Sign Up</button>
        </form>
    );
};