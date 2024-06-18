import './App.css'
import MainPage from './components/layouts/mainPage'

import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Quote from './components/pages/Quote';
import Partners from './components/pages/Partner';


function App() {

  return (
    <>
     <MainPage>
      <p>Aqui van los componentes Quote y Partner!! (debo sacarlos del header y dejar solo los botones)</p>
      <Router>
        <div>
          <Routes>
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
