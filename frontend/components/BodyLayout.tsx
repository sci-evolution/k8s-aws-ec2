"use client";

import React, { useState } from "react";
import Header from "./Header";
import Sidenav from "./Sidenav";
import Searchbar from "./Searchbar";
import MainContent from "./MainContent";
import Footer from "./Footer";

const BodyLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sidenavOpen, setSidenavOpen] = useState(false);
  const [searchbarOpen, setSearchbarOpen] = useState(false);

  return (
    <>
      <Header
        onToggleSidenav={() => setSidenavOpen((v) => !v)}
        onToggleSearchbar={() => setSearchbarOpen((v) => !v)}
      />
      <Sidenav open={sidenavOpen} onClose={() => setSidenavOpen(false)} />
      <Searchbar open={searchbarOpen} onClose={() => setSearchbarOpen(false)} onSearch={() => {}} />
      <MainContent>{children}</MainContent>
      <Footer />
    </>
  );
};

export default BodyLayout;
