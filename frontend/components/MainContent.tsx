import React, { ReactNode } from 'react';

type MainContentProps = {
  children: ReactNode;
};

const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <main style={{ margin: '2rem auto', maxWidth: 900, minHeight: '60vh', padding: '1rem' }}>
      {children}
    </main>
  );
};

export default MainContent;
