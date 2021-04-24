import buildClient from '../api/build-client';

const LandingPage = ({ currentUser }) => {
    console.log(currentUser);
    return <h1>Landing Page</h1>;
};

LandingPage.getInitialProps = async context => {
    const client = buildClient(context);
    const response = await client.get('/api/users/currentuser').catch(function (error) {
        if (error.response) {
            console.log('error autrh')
            const currentUser = null;
            return {  currentUser }
        }
    })
    const currentUser =response.data;
    return { currentUser }
};

export default LandingPage;