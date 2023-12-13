import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthContextProvider } from "./contexts/AuthContext";
 
import { Chat } from "./components/Chat";
import { Login } from "./components/Login";
import { Navbar } from "./components/Navbar";
 
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <AuthContextProvider>
              <Navbar />
            </AuthContextProvider>
          }
        >
          <Route path="" element={<Chat />} />
          <Route path="login" element={<Login />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}