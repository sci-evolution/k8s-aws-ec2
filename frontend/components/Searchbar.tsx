import React from 'react';

type SearchbarProps = {
  open: boolean;
  onClose: () => void;
  onSearch: () => void;
};

const Searchbar: React.FC<SearchbarProps> = ({ open, onClose, onSearch }) => {
  if (!open) return null;
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      background: 'rgba(0,0,0,0.4)',
      zIndex: 2000,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div style={{ background: '#fff', padding: '2rem', borderRadius: 8, minWidth: 320 }}>
        <input type="text" placeholder="Search..." style={{ width: '80%', padding: '0.5rem' }} />
        <button style={{ marginLeft: 8 }} onClick={onSearch}>Search</button>
        <button style={{ marginLeft: 8 }} onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default Searchbar;
