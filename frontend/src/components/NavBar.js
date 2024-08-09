import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCogs, faHome, faPlusCircle } from '@fortawesome/free-solid-svg-icons';
import '../styles/NavBar.css';
import logo from '../assets/logo.png'; // Adjust the path based on where you placed the logo

const NavBar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-logo">
                <img src={logo} alt="EchoPages Logo" className="navbar-logo-img" />
            </div>
            <ul className="navbar-links">
                <li>
                    <Link to="/" className="navbar-link">
                        <FontAwesomeIcon icon={faHome} className="navbar-icon" />
                        Home
                    </Link>
                </li>
                <li>
                    <Link to="/add-content" className="navbar-link">
                        <FontAwesomeIcon icon={faPlusCircle} className="navbar-icon" />
                        Add Content
                    </Link>
                </li>
                <li>
                    <Link to="/config" className="navbar-link">
                        <FontAwesomeIcon icon={faCogs} className="navbar-icon" />
                        Digest Configuration
                    </Link>
                </li>
            </ul>
        </nav>
    );
};

export default NavBar;