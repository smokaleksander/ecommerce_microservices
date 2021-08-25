import useRequest from "../../hooks/use-request";
import Router from 'next/router';

const SneakerShow = ({ sneaker }) => {
    const { doRequest, errors } = useRequest({
        url: `/api/orders/${sneaker._id}`,
        method: "post",
        body: {},
        onSuccess: (order) => Router.push('/orders/[orderId]', `/orders/${order._id}`)
    });

    return <div> 
        <h1>{ sneaker.brand }</h1>
        <h4>{ sneaker.model }</h4>
        <h5>Size: { sneaker.size } EU</h5>
        <h3>Price:{ sneaker.price }</h3>
        {errors}
        <button onClick={doRequest} className="btn btn-primary">Purchase</button>
    </div>;
};

SneakerShow.getInitialProps = async (context, client) => {
    const { sneakerId } = context.query;
    const { data } = await client.get(`/api/products/${sneakerId}`);

    return { sneaker: data }
};

export default SneakerShow;