const OrderIndex = ({ orders}) => {
    return (<div className="container">
        <h1>My Order</h1>
        <ul>
            {orders.map((order) => {
                return <li key={order._id}>
                    {order.product.brand} {order.product.model} | {order.status}
                </li>
            })}
        </ul>
        </div>
    );
}

OrderIndex.getInitialProps = async (context, client) => {
    //flag to prevent self signed tls cert error
    //happens couse of faked https on dev environment
    process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
    const { data } = await client.get('/api/orders/');

    return { orders: data}
};

export default OrderIndex;