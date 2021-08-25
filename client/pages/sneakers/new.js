import { useState } from 'react';
import useRequest from '../../hooks/use-request';
import Router from 'next/router';
import { route } from 'next/dist/next-server/server/router';
const NewSneakers = () => {
    const [brand, setBrand] = useState('');
    const [model, setModel] = useState('');
    const [size, setSize] = useState('');
    const [price, setPrice] = useState('');
    
    const onBlur = () => {
        const price_value = parseFloat(price);

        if (isNaN(price_value)) {   
            return;
        }
        setPrice(price_value.toFixed(2));
    };

    const { doRequest, errors } = useRequest({
        url: "/api/products/",
        method: "post",
        body: {
            brand, model, size, price
        },
        onSuccess: () => Router.push('/'),
    });

    const onSubmit = (event) => {
        event.preventDefault();
        doRequest();
    };

    return (<div>
        <h1>Add new pair of Sneakers</h1>
        <form onSubmit={onSubmit}>
            <div className="form-group">
                <label>Brand</label>
                <input value={brand} onChange={(e) => setBrand(e.target.value)} className="form-control"/>
            </div>
            <div className="form-group">
                <label>Model</label>
                <input value={model} onChange={(e) => setModel(e.target.value)} className="form-control"/>
            </div>
            <div className="form-group">
                <label>Size</label>
                <input value={size} onChange={(e) => setSize(e.target.value)} className="form-control"/>
            </div>
            <div className="form-group">
                <label>Price</label>
                <input value={price}
                    onBlur={onBlur} onChange={(e) => setPrice(e.target.value)} className="form-control"/>
            </div>
            {/* {errors} */}
            <button className="btn btn-primary">Submit</button>
        </form>
    </div>
    );
}
export default NewSneakers;