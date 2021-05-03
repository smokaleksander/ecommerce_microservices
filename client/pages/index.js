import buildClient from '../api/build-client';

const LandingPage = ({ currentUser }) => {
    
    return currentUser ? ( <h1>You are logged in</h1>) : ( <h1>You are not logged int</h1>);
};

LandingPage.getInitialProps = async context => {
    const client = buildClient(context);
    const response = await client.get('/api/users/currentuser').catch(function (error) {
        if (error.response) {
            const currentUser = null;
            return {  currentUser }
        }
    })
    const currentUser =response.data;
    return { currentUser }
};

export default LandingPage;