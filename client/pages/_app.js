import 'bootstrap/dist/css/bootstrap.css';
import buildClient from '../api/build-client';
import Header from '../components/header';

const AppComponent = ({ Component, pageProps, currentUser }) => {
    return (<dic>
        <Header currentUser= { currentUser }/>
        <Component {...pageProps} />
    </dic>);
    
};

AppComponent.getInitialProps = async appContext => {
    const client = buildClient(appContext.ctx);
    const response = await client.get('/api/users/currentuser').catch(function (error) {
        if (error.response) {
            const currentUser = null;
            return {  currentUser }
        }
    })
    let pageProps = {};
    if (appContext.Component.getInitialProps) {
        pageProps = await appContext.Component.getInitialProps(appContext.ctx);
    }
    const currentUser =response.data;
    return { 
        pageProps,
        currentUser 
    }
};

export default AppComponent;