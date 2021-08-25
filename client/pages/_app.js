import 'bootstrap/dist/css/bootstrap.css';
import buildClient from '../api/build-client';
import Header from '../components/header';

const AppComponent = ({ Component, pageProps, currentUser }) => {
    return (<dic>
        <Header currentUser= { currentUser }/>
        <div className="container">
            <Component currentUser= { currentUser } {...pageProps} />
        </div>
    </dic>);
    
};

AppComponent.getInitialProps = async appContext => {
    const client = buildClient(appContext.ctx);
    let currentUser = null
    const response = await client.get('/api/users/currentuser').catch(function (error) {
        if (error.response) {
            currentUser = null;
            return {  currentUser }
        }
    })
    if (response != undefined){
        currentUser = response.data;
    }
    let pageProps = {};
    if (appContext.Component.getInitialProps) {
        pageProps = await appContext.Component.getInitialProps(appContext.ctx, client, currentUser);
    }
    
    return { 
        pageProps,
        currentUser 
    }
};

export default AppComponent;