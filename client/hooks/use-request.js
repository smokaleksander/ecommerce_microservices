import axios from 'axios';
import { useState } from 'react';

const req =  ({ url, method, body,config, onSuccess }) => {
    const [errors, setErrors] =  useState(null);

    const doRequest = async (props = {}) => {
        console.log({...props})
        try {
            setErrors(null);
            const response = await axios[method](url,{
                ...body, ...props
            });

            if (onSuccess) {
                onSuccess(response.data);
            }
            return response.data;
        } catch (err) {
            console.log(err)
            setErrors(
                <div className='alert-danger'>
                <h4>Something went wrong...</h4>
                <ul className='my-0'>
                    {(err.response.data.errors).map(err => (
                        <li key={err.message}>{err.msg}</li>
                    ))}
                </ul>
            </div>
            );
        }
    };

    return { doRequest, errors };
}

export default req;