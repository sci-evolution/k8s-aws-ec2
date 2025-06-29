import React from 'react';
import AppLogo from './AppLogo';

type HeaderProps = {
  onToggleSidenav: () => void;
  onToggleSearchbar: () => void;
};

const Header: React.FC<HeaderProps> = ({ onToggleSidenav, onToggleSearchbar }) => {
  return (
    <header style={{ display: 'flex', alignItems: 'center', padding: '1rem', background: '#222', color: '#fff' }}>
      <button onClick={onToggleSidenav} aria-label="Open navigation" style={{ fontSize: '1.5rem', marginRight: '1rem' }}>
        &#9776;
      </button>
      <AppLogo />
      <div style={{ flex: 1 }} />
      <button onClick={onToggleSearchbar} aria-label="Open search" style={{ fontSize: '1.5rem' }}>
        🔍
      </button>
    </header>
  );
};

export default Header;
