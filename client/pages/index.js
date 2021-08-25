import Link from 'next/link';

const LandingPage = ({ currentUser, sneakers }) => {
    const sneakersList = sneakers.map(sneaker => {
        return (
            <tr key={sneaker._id}>
                <td>{sneaker.brand}</td>
                <td>{sneaker.model}</td>
                <td>{sneaker.size}</td>
                <td>{sneaker.price}</td>
                <td>
                    <Link href="/sneakers/[sneakerId]" as={`/sneakers/${sneaker._id}`}>
                        <a>View</a>
                    </Link>
                </td>
            </tr>

        )
    })
    
    return (
        <div>
            <h1> Sneakers</h1>
            <table className="table">
                <thead>
                    <tr>
                        <th>Brand</th>
                        <th>Model</th>
                        <th>EU Size</th>
                        <th>Price $</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
                    {sneakersList}
                </tbody>
            </table>
        </div>
    );
};

LandingPage.getInitialProps = async (context, client, currentUser) => {
    //flag to prevent self signed tls cert error
    //happens couse of faked https on dev environment
    process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
    const { data } = await client.get('/api/products/');

    return { sneakers: data}
};

export default LandingPage;