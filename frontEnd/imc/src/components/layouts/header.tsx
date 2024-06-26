import { NavLink } from 'react-router-dom';
import './Header.css'; // Assuming you have some styles for the header

function Header() {
  return (
    <>
      <p>Data Loader for IMC Storage. Please select which data you would like to upload.</p>
      <nav className="nav">
        <NavLink to="/quote" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Quote
        </NavLink>
        <NavLink to="/partners" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Partners
        </NavLink>
      </nav>
    </>
  );
}

export default Header;
