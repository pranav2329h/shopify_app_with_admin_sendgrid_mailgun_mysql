// src/Install.tsx
import React, { useState } from "react";
import "./Install.css";

const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL ?? "http://localhost:5173"; // set in admin-vite/.env

export default function Install() {
  const [shop, setShop] = useState("");

  function normalizeShop(input: string) {
    let s = input.trim();
    s = s.replace(/^https?:\/\//i, "").replace(/\/+$/g, ""); // strip protocol & trailing slash
    if (!s.endsWith(".myshopify.com")) s = `${s}.myshopify.com`;
    return s.toLowerCase();
  }

  function isValidShop(s: string) {
    return /^[a-z0-9][a-z0-9-]*\.myshopify\.com$/i.test(s);
  }

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); // stop full page reload
    const normalized = normalizeShop(shop);
    if (!isValidShop(normalized)) {
      alert("Enter a valid domain like your-store.myshopify.com");
      return;
    }
    window.location.href = `${BACKEND_URL}/auth/install?shop=${encodeURIComponent(
      normalized
    )}`;
  }

  return (
    <div className="container">
      <h1>Silvee 925 – Auto Email App</h1>
      <form onSubmit={onSubmit} noValidate>
        <label htmlFor="shop">Shop domain</label>
        <input
          id="shop"
          name="shop"
          type="text"
          value={shop}
          onChange={(e) => setShop(e.target.value)}
          placeholder="your-store.myshopify.com"
          autoComplete="off"
          required
        />
        <small>Permanent domain (e.g., my-store.myshopify.com)</small>
        <button type="submit">Connect Store</button>
      </form>
    </div>
  );
}
