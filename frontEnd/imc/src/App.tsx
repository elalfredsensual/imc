import './App.css'
import MainPage from './components/layouts/mainPage'

import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";

import Quote from './components/pages/Quote';
import Partners from './components/pages/Partner';
import HelloWorld from './components/pages/HelloWorld';


function App() {

  return (
    <>
    <header>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </header>
     <MainPage>
      <p>Aqui van los componentes Quote y Partner!! (debo sacarlos del header y dejar solo los botones)</p>
      <Router>
        <div>
          <Routes>
              <Route path="/" Component={HelloWorld} />
              <Route path="/quote" element={<Quote />} />
              <Route path="/partners" element={<Partners />} />
          </Routes>
        </div>
      </Router>
    </MainPage> 
    </>
  )
}

export default App
