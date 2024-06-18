//componente de la pagina principal que contiene el header, children y footer
import React from 'react';
import Header from './header';
import Footer from './footer';

interface MainPageProps {
    children: React.ReactNode;
}

const MainPage: React.FC<MainPageProps> = ({ children }) => {
    return (
        <div>
            <Header />
            <main>{children}</main>
            <Footer />
        </div>
    );
};

export default MainPage;