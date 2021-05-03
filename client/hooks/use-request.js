import axios from 'axios';
import { useState } from 'react';

export default ({ url, method, body,config, onSuccess }) => {
    const [errors, setErrors] =  useState(null);

    const doRequest = async () => {
        try {
            setErrors(null);
            const response = await axios[method](url, body, config);

            if (onSuccess) {
                onSuccess(response.data);
            }
            return response.data;
        } catch (err) {
            setErrors(
                <div className='alert-danger'>
                <h4>Something went wrong...</h4>
                <ul className='my-0'>
                    {err.response.data.errors.map(err => (
                        <li key={err.message}>{err.msg}</li>
                    ))}
                </ul>
            </div>
            );
        }
    };

    return { doRequest, errors };
}
