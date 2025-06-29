import React from 'react';
import Link from 'next/link';

type SidenavProps = {
  open: boolean;
  onClose: () => void;
};

const Sidenav: React.FC<SidenavProps> = ({ open, onClose }) => {
  return (
    <nav style={{
      width: open ? 220 : 0,
      transition: 'width 0.2s',
      overflow: 'hidden',
      background: '#333',
      color: '#fff',
      height: '100vh',
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 1000,
      paddingTop: '4rem',
    }}>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        <li><Link href="/" style={{ color: '#fff', textDecoration: 'none', display: 'block', padding: '1rem' }}>Tasks</Link></li>
        <li><Link href="/tasks/new" style={{ color: '#fff', textDecoration: 'none', display: 'block', padding: '1rem' }}>New Task</Link></li>
        {/* Add more navigation links here */}
      </ul>
      <button onClick={onClose} style={{ position: 'absolute', top: 10, right: 10, background: 'none', color: '#fff', border: 'none', fontSize: '1.5rem' }}>&times;</button>
    </nav>
  );
};

export default Sidenav;
