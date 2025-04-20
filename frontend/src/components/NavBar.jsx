"use client"

import { useState } from "react"
import { Link } from "react-router-dom"

const NavBar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-content">
          {/* Logo */}
          <Link to="/" className="navbar-logo">
            <img
              src="/images/CarValue-Predictor-Logo-Design.png"
              alt="CarValue Predictor Logo"
              className="logo-image"
            />
          </Link>

          {/* Desktop Menu */}
          <div className="navbar-links">
            <Link to="/" className="nav-link">
              Home
            </Link>
            <Link to="/predictor" className="nav-link">
              Price Estimator
            </Link>
            <Link to="/about" className="nav-link">
              About
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="mobile-menu-button">
            <button onClick={toggleMenu} aria-label="Toggle menu">
              <svg className="menu-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="mobile-menu">
            <Link to="/" className="mobile-menu-link" onClick={() => setIsMenuOpen(false)}>
              Home
            </Link>
            <Link to="/predictor" className="mobile-menu-link" onClick={() => setIsMenuOpen(false)}>
              Price Estimator
            </Link>
            <Link to="/about" className="mobile-menu-link" onClick={() => setIsMenuOpen(false)}>
              About
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default NavBar
