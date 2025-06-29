import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer style={{ padding: '1rem', background: '#222', color: '#fff', textAlign: 'center' }}>
      &copy; {new Date().getFullYear()} Task Manager. All rights reserved.
    </footer>
  );
};

export default Footer;
